import cv2
import os
from ultralytics import YOLO

def process_video(
        video_path,
        clean_folder,
        dusty_folder,
        damaged_folder,
        solar_rows,
        solar_columns,
        model_path,
        mission_video_id,
        framesToKeep,
        insert_mission_data_image,
        margin=10,
        confidence_threshold=0.4
):
    model = YOLO(model_path)
    class_names = ['clean_solar_panel', 'dusty_solar_panel', 'damaged_solar_panel']

    cap = cv2.VideoCapture(video_path)

    counts = {
        'total': 0,
        'clean': 0,
        'dusty': 0,
        'damaged': 0
    }

    grid = {}
    grid_row = 0
    grid_col = 0
    frames = 0
    reverse = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frames in framesToKeep:
            print(f"Processing frame {frames}")
            results = model(frame)

            current_frame_classes = set()
            frame_height, frame_width = frame.shape[:2]

            for result in results:
                boxes = result.boxes.xyxy.cpu().numpy()
                confs = result.boxes.conf.cpu().numpy()
                cls_ids = result.boxes.cls.cpu().numpy().astype(int)

                for box, conf, cls_id in zip(boxes, confs, cls_ids):
                    if conf < confidence_threshold:
                        continue

                    x1, y1, x2, y2 = map(int, box)

                    if (
                        x1 <= margin or
                        y1 <= margin or
                        x2 >= frame_width - margin or
                        y2 >= frame_height - margin
                    ):
                        continue

                    panel_class = class_names[cls_id]
                    current_frame_classes.add(panel_class)

                    color = (0, 255, 0) if cls_id == 0 else (0, 165, 255) if cls_id == 1 else (0, 0, 255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                    # Text: class name + confidence
                    cv2.putText(frame, f"{panel_class} {conf:.2f}",
                                (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                    # ➕ Center of the bounding box: display grid_row, grid_col
                    center_x = int((x1 + x2) / 2)
                    center_y = int((y1 + y2) / 2)
                    cv2.putText(frame, f"{grid_row},{grid_col}", (center_x - 20, center_y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 64, 253), 2)

                    if panel_class == 'clean_solar_panel':
                        counts['clean'] += 1
                    elif panel_class == 'dusty_solar_panel':
                        counts['dusty'] += 1
                    elif panel_class == 'damaged_solar_panel':
                        counts['damaged'] += 1
                    counts['total'] += 1

            print(f' current row is {grid_row}')
            print(f'current col is {grid_col}')
            cv2.imshow("Prediction", frame)
            print(">> Press any key to continue...")
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            frame_filename = f"frame_{frames:04d}.jpg"

            if 'clean_solar_panel' in current_frame_classes:
                image_path = os.path.join(clean_folder, frame_filename)
                cv2.imwrite(image_path, frame)
                insert_mission_data_image({
                    'mission_video_id': mission_video_id,
                    'image_path': image_path,
                    'solar_row': grid_row,
                    'solar_column': grid_col,
                    'label': 'clean_solar_panel'
                })

            if 'dusty_solar_panel' in current_frame_classes:
                image_path = os.path.join(dusty_folder, frame_filename)
                cv2.imwrite(image_path, frame)
                insert_mission_data_image({
                    'mission_video_id': mission_video_id,
                    'image_path': image_path,
                    'solar_row': grid_row,
                    'solar_column': grid_col,
                    'label': 'dusty_solar_panel'
                })

            if 'damaged_solar_panel' in current_frame_classes:
                image_path = os.path.join(damaged_folder, frame_filename)
                cv2.imwrite(image_path, frame)
                insert_mission_data_image({
                    'mission_video_id': mission_video_id,
                    'image_path': image_path,
                    'solar_row': grid_row,
                    'solar_column': grid_col,
                    'label': 'damaged_solar_panel'
                })

            if reverse:
                grid_col -= 1
            else:
                grid_col += 1

            if grid_col == solar_columns:
                grid_col -= 1
                grid_row += 1
                reverse = True
            elif grid_col == -1:
                grid_row += 1
                reverse = False

        frames += 1

    cap.release()
    cv2.destroyAllWindows()

    print(f"Video processing complete. Total panels: {counts['total']}, "
          f"clean: {counts['clean']}, dusty: {counts['dusty']}, damaged: {counts['damaged']}")

    return counts, grid