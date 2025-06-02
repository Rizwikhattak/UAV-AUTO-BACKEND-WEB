from ultralytics import YOLO
import cv2
import numpy as np
import os
from Controller import MissionDataLocationController, MissionDataImageController
import random
import math
from Model import  LocationPin,MissionPlanner,Drone,MissionDataLocation,MissionDataImage


model = YOLO(r'C:\Users\Muhammad Rizwan\PycharmProjects\UAVAUTO\CVModel\weights\best.pt')  # Path to your trained weights



def extract_frames(data, output_folder, frames_per_second=5):
    start_location = LocationPin.query.filter_by(id=data['location_pin_id'],validity=1).first()
    end_location = LocationPin.query.filter_by(id=data['end_location_pin_id'],validity=1).first()
    mission_planner = MissionPlanner.query.filter_by(id=data['mission_planner_id']).first()
    drone = Drone.query.filter_by(id=mission_planner.drone_id).first()

    if not (start_location and end_location and mission_planner and drone):
        print("Error: Missing database data for processing.")
        return {}

    # Video properties and constants
    cap = cv2.VideoCapture(data['video_path'])
    if not cap.isOpened():
        print("Error: Unable to open video.")
        return {}

    start_lat, start_lon = start_location.latitude, start_location.longitude
    end_lat, end_lon = end_location.latitude, end_location.longitude
    speed = drone.speed  # Drone speed in meters per second
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    video_length = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps  # Video length in seconds

    frame_count, saved_frame_count = 0, 0
    current_second_frames = []
    current_second = 0
    all_mission_data_locations_data = []


    def process_and_save(selected_frames, second):
        nonlocal saved_frame_count
        chk = True
        temp = {}
        mission_data_location = {}
        print("selected_frames :",len(selected_frames))
        for i, frame in enumerate(selected_frames):
            plotted_image, class_label, isDamaged, confidence_score = process_single_image(frame)
            if isDamaged:
                damage_lat, damage_lon = get_damage_coordinates(
                    start_lat, start_lon, end_lat, end_lon, speed, fps, second * fps + i, video_length
                )
                print(f"Damage Detected: {class_label} at Lat: {damage_lat}, Lon: {damage_lon}")

                if chk:
                    mission_data_location = MissionDataLocationController.insert_mission_data_location({'mission_video_id':data['mission_video_id'],'latitude':damage_lat,'longitude':damage_lon,'damage':class_label})
                    temp['mission_data_location_id'] = mission_data_location.get('id')
                    temp['latitude'] = mission_data_location.get('latitude')
                    temp['longitude'] = mission_data_location.get('longitude')
                    temp['damage'] = mission_data_location.get('damage')
                    temp['image_paths'] = []
                    chk = False
                damaged_frame_file_path = os.path.join(
                    output_folder, f"{mission_data_location.get('id')}_{second}_{class_label}_{confidence_score:.2f}.png"
                )
                cv2.imwrite(damaged_frame_file_path, plotted_image)
                damaged_frame_file_path = damaged_frame_file_path.replace("\\","/")
                mission_data_image = MissionDataImageController.insert_mission_data_image({'mission_data_location_id':mission_data_location.get('id'),'image_path':damaged_frame_file_path})
                temp['image_paths'].append(mission_data_image.get('image_path'))
                saved_frame_count += 1
        if temp:
            all_mission_data_locations_data.append(temp)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_second = frame_count // fps

        if frame_second != current_second:
            if current_second_frames:
                print("current second frames:",len(current_second_frames))
                selected_frames = random.sample(
                    current_second_frames, min(frames_per_second, len(current_second_frames))
                )
                print("Selected Frames", len(selected_frames))
                process_and_save(selected_frames, current_second)

            current_second_frames = []
            current_second = frame_second

        current_second_frames.append(frame)
        frame_count += 1

    # Process remaining frames for the last second
    if current_second_frames:
        selected_frames = random.sample(
            current_second_frames, min(frames_per_second, len(current_second_frames))
        )
        process_and_save(selected_frames, current_second)

    cap.release()
    print(f"Total frames saved: {saved_frame_count}")
    return all_mission_data_locations_data


def process_single_image(img):
    """
    Process a single image using YOLO and return results.
    """
    result = model.predict(source=img, save=False)
    plotted_image = []
    isDamaged = False
    class_label = ''
    confidence_score = 0.0

    for r in result:
        labels = r.names
        bboxes = r.boxes.xyxy
        confidences = r.boxes.conf
        class_ids = r.boxes.cls

        for cls, conf in zip(class_ids, confidences):
            cls = int(cls)
            if labels[cls].split("_")[0] in ['damaged', 'loose']:
                isDamaged = True
                class_label = labels[cls]
                confidence_score = float(conf)
            plotted_image = r.plot()

    return plotted_image, class_label, isDamaged, confidence_score


# Function to calculate intermediate latitude and longitude using spherical interpolation
def calculate_intermediate_coordinates(start_lat, start_lon, end_lat, end_lon, fraction):

    start_lat_rad = math.radians(start_lat)
    start_lon_rad = math.radians(start_lon)
    end_lat_rad = math.radians(end_lat)
    end_lon_rad = math.radians(end_lon)

    # Compute the angular distance between the two points
    delta_sigma = math.acos(
        math.sin(start_lat_rad) * math.sin(end_lat_rad) +
        math.cos(start_lat_rad) * math.cos(end_lat_rad) * math.cos(end_lon_rad - start_lon_rad)
    )

    # Handle the case where the two points are the same
    if delta_sigma == 0:
        return start_lat, start_lon

    # Compute the intermediate point
    a = math.sin((1 - fraction) * delta_sigma) / math.sin(delta_sigma)
    b = math.sin(fraction * delta_sigma) / math.sin(delta_sigma)

    x = a * math.cos(start_lat_rad) * math.cos(start_lon_rad) + b * math.cos(end_lat_rad) * math.cos(end_lon_rad)
    y = a * math.cos(start_lat_rad) * math.sin(start_lon_rad) + b * math.cos(end_lat_rad) * math.sin(end_lon_rad)
    z = a * math.sin(start_lat_rad) + b * math.sin(end_lat_rad)

    # Convert back to latitude and longitude
    intermediate_lat = math.atan2(z, math.sqrt(x ** 2 + y ** 2))
    intermediate_lon = math.atan2(y, x)

    # Convert radians to degrees
    intermediate_lat = math.degrees(intermediate_lat)
    intermediate_lon = math.degrees(intermediate_lon)

    return intermediate_lat, intermediate_lon


# Main function to calculate damage coordinates
def get_damage_coordinates(start_lat, start_lon, end_lat, end_lon, speed, fps, damage_frame, video_length):
    """
    Get the latitude and longitude of damage detected in a video.

    Args:
        start_lat (float): Starting latitude in decimal degrees.
        start_lon (float): Starting longitude in decimal degrees.
        end_lat (float): Ending latitude in decimal degrees.
        end_lon (float): Ending longitude in decimal degrees.
        speed (float): Drone speed in meters per second.
        fps (int): Frames per second of the video.
        damage_frame (int): Frame number where damage is detected.
        video_length (float): Total length of the video in seconds.

    Returns:
        (float, float): Latitude and longitude of the detected damage.
    """
    # Calculate the fraction of distance traveled at the damage frame
    distance_fraction = damage_frame / (fps * video_length)

    # Calculate the intermediate coordinates
    damage_lat, damage_lon = calculate_intermediate_coordinates(
        start_lat, start_lon, end_lat, end_lon, distance_fraction
    )

    return damage_lat, damage_lon


# # Example Usage
# if __name__ == "__main__":
#     # Starting GPS coordinates (Shamsabad Metro Station)
#     start_lat = 33.65020799590798
#     start_lon = 73.07990132383055
#
#     # Ending GPS coordinates (Rehmanabad Metro Station)
#     end_lat = 33.63634560089784
#     end_lon = 73.0749241949942
#
#     # 33.65020799590798, 33.65020799590798 Shamsabad metro station
#     # Ending GPS coordinates
#     # 33.63634560089784, 73.0749241949942 Rehmanabad metro station
#
#     # Drone properties
#     speed = 10  # Drone speed in meters per second
#     fps = 30  # Video FPS
#     video_length = 60  # Video length in seconds
#     damage_frame = 600  # Frame where damage is detected
#
#     # Get damage coordinates
#     damage_lat, damage_lon = get_damage_coordinates(start_lat, start_lon, end_lat, end_lon, speed, fps, damage_frame, video_length)
#     print(f"Damage Coordinates: Latitude = {damage_lat}, Longitude = {damage_lon}")
#

# # Function to calculate bearing between two points
# def calculate_bearing(start_lat, start_lon, end_lat, end_lon):
#     """
#     Calculate the initial bearing between two geographic coordinates.
#
#     Args:
#         start_lat (float): Starting latitude in decimal degrees.
#         start_lon (float): Starting longitude in decimal degrees.
#         end_lat (float): Ending latitude in decimal degrees.
#         end_lon (float): Ending longitude in decimal degrees.
#
#     Returns:
#         float: Initial bearing in degrees from north.
#     """
#     # Convert coordinates to radians
#     start_lat = math.radians(start_lat)
#     start_lon = math.radians(start_lon)
#     end_lat = math.radians(end_lat)
#     end_lon = math.radians(end_lon)
#
#     # Calculate differences
#     delta_lon = end_lon - start_lon
#
#     # Calculate the bearing
#     x = math.sin(delta_lon) * math.cos(end_lat)
#     y = math.cos(start_lat) * math.sin(end_lat) - math.sin(start_lat) * math.cos(end_lat) * math.cos(delta_lon)
#     bearing = math.atan2(x, y)
#
#     # Convert from radians to degrees and normalize
#     bearing = math.degrees(bearing)
#     bearing = (bearing + 360) % 360  # Normalize to 0-360 degrees
#
#     return bearing

# def extract_frames(video_path,output_folder,extract_interval=1):
#     cap = cv2.VideoCapture(video_path)
#     # Get the frame rate (FPS) of the video
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     print(f"Frames per second: {fps}")
#
#     # Calculate frame interval (number of frames to skip)
#     frame_interval = fps * extract_interval
#     frame_count = 0
#     saved_frame_count = 0
#     while True:
#         ret,frame = cap.read()
#         if not ret:
#             break
#         if frame_count % frame_interval == 0:
#             plotted_image,isDamaged = process_single_image(frame)
#             frame_file_name = os.path.join(output_folder,f"frame_{saved_frame_count}.jpeg")
#             cv2.imwrite(frame_file_name,plotted_image)
#             saved_frame_count+=1
#             # if isDamaged:
#             #     frame_file_name = os.path.join(output_folder,f"frame_{saved_frame_count}.jpeg")
#             #     cv2.imwrite(frame_file_name,plotted_image)
#             #     saved_frame_count+=1
#         frame_count+=1
#
#     cap.release()
#     print(f"saved frame count is:{saved_frame_count}")
#
# def process_single_image(img):
#     # Convert image from file to array
#     # img_array = np.frombuffer(image.read(), np.uint8)
#     # img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#
#     # Predict using YOLO model
#     result = model.predict(source=img, save=False)
#     plotted_image = []
#     isDamaged = False
#     for r in result:
#         # Get labels, bounding boxes, and confidence scores
#         labels = r.names  # Predicted class names
#         bboxes = r.boxes.xyxy  # Bounding boxes (x_min, y_min, x_max, y_max)
#         confidences = r.boxes.conf  # Confidence scores
#         class_ids = r.boxes.cls  # Class IDs
#         class_label = ''
#         # print("Labels:", labels)
#         # print("Bounding Boxes:", bboxes)
#         # print("Confidence Scores:", confidences)
#         # print("Class IDs:", class_ids)
#         for cls in class_ids:
#             cls = int(cls)
#             if(labels[cls].split("_")[0]=='damaged' or labels[cls].split("_")[0]=='loose'):
#                 # Plot and display the predictions
#                 isDamaged = True
#             class_label = labels[cls]
#             plotted_image = r.plot()
#
#         # cv2.imshow('Predictions', plotted_image)
#         # cv2.waitKey(0)
#         # cv2.destroyAllWindows()
#
#     # temp_path = os.path.join(app.config['TEMP_FOLDER'], "processed_image.jpg")
#     # cv2.imwrite(temp_path, plotted_image)
#     # Get the absolute path
#     # absolute_path = os.path.abspath(temp_path)
#     if isDamaged:
#         return plotted_image,class_label,True
#     else:
#         return plotted_image,class_label,False



# Function to process a single image

# def process_single_image(image):
#     # Convert image from file to array
#     img_array = np.frombuffer(image.read(), np.uint8)
#     img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#
#     # Predict using YOLO model
#     result = model.predict(source=img, save=False)
#     plotted_image = []
#     isDamaged = False
#     for r in result:
#         # Get labels, bounding boxes, and confidence scores
#         labels = r.names  # Predicted class names
#         bboxes = r.boxes.xyxy  # Bounding boxes (x_min, y_min, x_max, y_max)
#         confidences = r.boxes.conf  # Confidence scores
#         class_ids = r.boxes.cls  # Class IDs
#
#         print("Labels:", labels)
#         print("Bounding Boxes:", bboxes)
#         print("Confidence Scores:", confidences)
#         print("Class IDs:", class_ids)
#         for cls in class_ids:
#             cls = int(cls)
#             if(labels[cls]=='damaged_pole' or labels[cls]=='damaged_wire' or labels[cls]=='damaged_insulator' or labels[cls]=='loose_wire'):
#                 # Plot and display the predictions
#                 plotted_image = r.plot()
#                 isDamaged = True
#
#         # cv2.imshow('Predictions', plotted_image)
#         # cv2.waitKey(0)
#         # cv2.destroyAllWindows()
#
#     temp_path = os.path.join(app.config['TEMP_FOLDER'], "processed_image.jpg")
#     cv2.imwrite(temp_path, plotted_image)
#     # Get the absolute path
#     absolute_path = os.path.abspath(temp_path)
#     if isDamaged:
#         return absolute_path,True
#     else:
#         return absolute_path,False
#     # return result

# def process_multiple_images(images):
#     processed_paths = []
#     for image in images:
#         # Process each image
#         img_array = np.frombuffer(image.read(), np.uint8)
#         img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#         result = model.predict(source=img, save=False)
#
#         # Plot predictions
#         for pred_img in result:
#             processed_img = pred_img.plot()
#
#         # Save each processed image temporarily
#         temp_path = os.path.join(app.config['TEMP_FOLDER'], f"processed_image_{len(processed_paths)}.jpg")
#         cv2.imwrite(temp_path, processed_img)
#         processed_paths.append(temp_path)
#
#     return processed_paths
