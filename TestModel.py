import cv2
from ultralytics import YOLO

def run_yolo_on_video(video_path, model_path, confidence=0.5):
    # Load the YOLOv8 model
    model = YOLO(model_path)

    # Open the video
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # End of video

        # Run YOLOv8 inference on the frame
        results = model(frame, conf=confidence)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Optional: Resize if too big
        scale_percent = 70  # Resize to 70% of original size
        width = int(annotated_frame.shape[1] * scale_percent / 100)
        height = int(annotated_frame.shape[0] * scale_percent / 100)
        resized_frame = cv2.resize(annotated_frame, (width, height))

        # Display the frame
        cv2.imshow('YOLOv8 - Solar Panel Detection', resized_frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# # Run the function
# run_yolo_on_video(
#     r"D:\UNIVERSITY PROJECT\Aina.MP4",
#     r"D:\UNIVERSITY PROJECT\UAV-AUTO-BACKEND-WEB\yolo11x_solar\weights\best.pt",
#     confidence=0.4
# )

# import cv2

# import cv2

def show_video_frames(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Cannot open video.")
        return

    frame_count = 0
    cv2.namedWindow("Video Frame", cv2.WINDOW_NORMAL)  # Make window resizable

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video.")
            break

        frame_count += 1
        print(f"Frame {frame_count}")

        cv2.imshow("Video Frame", frame)

        key = cv2.waitKey(0)
        if key == ord('q'):
            print("Quitting...")
            break

    cap.release()
    cv2.destroyAllWindows()




# Example usage:
# show_video_frames(r"C:\Users\rizwi\Downloads\All Video\Rizwan1.MP4")


import cv2
from ultralytics import YOLO  # Make sure ultralytics is installed: pip install ultralytics

def show_video_frames_with_yolo(video_path, model_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Cannot open video.")
        return

    # Load YOLO model
    model = YOLO(model_path)
    print("YOLO model loaded.")

    frame_count = 0
    cv2.namedWindow("Video Frame", cv2.WINDOW_NORMAL)  # Allow resize

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video.")
            break

        frame_count += 1
        print(f"Frame {frame_count}")

        # Run YOLO inference on the frame
        results = model(frame)[0]  # Get the first result

        # Draw the bounding boxes and labels
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordinates
            conf = box.conf[0]
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            print("names",model.names)
            # Draw rectangle
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Video Frame", frame)

        key = cv2.waitKey(0)
        if key == ord('q'):
            print("Quitting...")
            break

    cap.release()
    cv2.destroyAllWindows()


video_path = r"D:\UNIVERSITY PROJECT\Aina.MP4"
model_path = r"D:\UNIVERSITY PROJECT\UAV-AUTO-BACKEND-WEB\yolo11x_solar\weights\best.pt"  # Replace with your model path

show_video_frames_with_yolo(video_path, model_path)
