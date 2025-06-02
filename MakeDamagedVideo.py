from ultralytics import YOLO
model = YOLO(r"D:\UNIVERSITY PROJECT\uavauto_aina\yolov8n\weights\best.pt")

# first call – registers trackers internally
results = model.track(source=r"C:\Users\rizwi\Downloads\solar_farm_drone_view.mp4", tracker="bytetrack.yaml", persist=True)

print("Trackers dict now exists:", model.trackers)  # ✅

# import cv2
# import random
# import os
# import torch
# from torch.serialization import add_safe_globals
# from ultralytics.nn.tasks import DetectionModel
# add_safe_globals([DetectionModel])       # allowlist the class
# from ultralytics import YOLO
# import cv2
# import random
# import os
# import torch, sys, ultralytics
#
# def MakeDamagedVideo(video_path, damaged_frame_path, output_path, insert_duration=1, insert_second=0):
#     """
#     Inserts a damaged frame into a video at a specified second for a given duration.
#
#     Args:
#         video_path (str): Path to the original video.
#         damaged_frame_path (str): Path to the damaged frame image.
#         output_path (str): Path to save the output video.
#         insert_duration (int): Duration in seconds to insert the damaged frame.
#         insert_second (int): The exact second in the video where the damaged frame should be inserted.
#
#     Returns:
#         str: Path to the output video.
#     """
#     # Open the video file
#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         raise Exception(f"Unable to open video: {video_path}")
#
#     # Get video properties
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     insert_frames = fps * insert_duration
#
#     # Convert insert_second to frame number
#     insert_start_frame = insert_second * fps
#     if insert_start_frame + insert_frames > total_frames:
#         raise ValueError("Insert duration exceeds video length at the specified second.")
#
#     # Load the damaged frame
#     damaged_frame = cv2.imread(damaged_frame_path)
#     damaged_frame = cv2.resize(damaged_frame, (frame_width, frame_height))
#
#     # Prepare the output video writer
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
#
#     # Write frames to the output video
#     frame_count = 0
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         # Insert the damaged frame for the specified duration
#         if insert_start_frame <= frame_count < insert_start_frame + insert_frames:
#             out.write(damaged_frame)
#         else:
#             out.write(frame)
#
#         frame_count += 1
#
#     cap.release()
#     out.release()
#     return output_path
#
#
# def MakeVideoFromImages(image_paths, output_path, fps=30, duration_per_image=1):
#     """
#     Creates a video by repeating each image for a specified duration.
#
#     Args:
#         image_paths (list): List of paths to the images.
#         output_path (str): Path to save the output video.
#         fps (int): Frames per second for the output video.
#         duration_per_image (int): Duration for each image in seconds.
#
#     Returns:
#         str: Path to the output video.
#     """
#     if not image_paths:
#         raise ValueError("Image paths array is empty")
#
#     # Load the first image to get dimensions
#     sample_image = cv2.imread(image_paths[0])
#     frame_height, frame_width, _ = sample_image.shape
#
#     # Prepare the output video writer
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
#
#     # Repeat each image for the specified duration
#     frames_per_image = fps * duration_per_image
#     for image_path in image_paths:
#         img = cv2.imread(image_path)
#         img = cv2.resize(img, (frame_width, frame_height))
#
#         for _ in range(frames_per_image):
#             out.write(img)
#
#     out.release()
#     return output_path
#
#
# if __name__ == "__main__":
#     print("Torch :", torch.__version__)
#     print("Ultralytics:", ultralytics.__version__)
#
#     m = YOLO(r"best.pt")  # should load without error
#     print(m.trackers['bytetrack'])
#
#     # m = YOLO(r'D:\UNIVERSITY PROJECT\uavauto_aina\yolov8n\weights\best.pt')
#     # print("Hi nice",m.trackers)
#
#     # from ultralytics import YOLO
#     # import cv2, numpy as np
#     #
#     # model = YOLO(model_path)
#     # for r in model.track(source='sample.mp4', show=False, stream=True, persist=True):
#     #     frame = r.plot()  # annotated
#     #     ids = r.boxes.id.cpu().tolist()
#     #     print(f'frame {r.names}: IDs={ids}')
#     #     if cv2.waitKey(1) == 27:
#     #         break
#
#     # Test MakeDamagedVideo
#     # video_path = r"C:\Users\Muhammad Rizwan\PycharmProjects\UAVAUTO\damaged_video4.mp4"
#     # damaged_frame_path = r"C:\Users\Muhammad Rizwan\Downloads\Poles_Images\Poles_Images\damaged_pole_4.webp"
#     # damaged_video_output = r"C:\Users\Muhammad Rizwan\PycharmProjects\UAVAUTO\damaged_video5.mp4"
#     #
#     # try:
#     #     result = MakeDamagedVideo(video_path, damaged_frame_path, damaged_video_output, insert_duration=2, insert_second=20)
#     #     print(f"Damaged video created at: {result}")
#     # except Exception as e:
#     #     print(f"Error creating damaged video: {e}")
#
#     # # Test MakeVideoFromImages
#     # image_paths = ["image1.jpg", "image2.jpg", "image3.jpg"]
#     # images_video_output = "path_to_output_images_video.mp4"
#     #
#     # try:
#     #     result = MakeVideoFromImages(image_paths, images_video_output, fps=30, duration_per_image=1)
#     #     print(f"Video from images created at: {result}")
#     # except Exception as e:
#     #     print(f"Error creating video from images: {e}")
