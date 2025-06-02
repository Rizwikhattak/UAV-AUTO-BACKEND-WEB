import cv2
import os
import numpy as np
import torch
from ultralytics import YOLO
import random
import json
from collections import defaultdict
from Controller import MissionPlannerController

def process_video(
        video_path,
        clean_folder,
        dusty_folder,
        damaged_folder,
        solar_rows,
        solar_columns,
        model_path,
        mission_video_id
):
    """
    Process a video to detect and classify solar panels using YOLOv8.

    Args:
        video_path: Path to the input video
        clean_folder: Path to save clean solar panel images
        dusty_folder: Path to save dusty solar panel images
        damaged_folder: Path to save damaged solar panel images
        solar_rows: Number of rows in the solar grid
        solar_columns: Number of columns in the solar grid
        model_path: Path to YOLOv8 model weights

    Returns:
        counts: Dictionary with counts of different types of solar panels
        grid: Dictionary with grid positions and panel conditions
    """
    # Load the YOLOv8 model
    model = YOLO(model_path)

    # Labels mapping
    class_names = ['clean_solar_panel', 'dusty_solar_panel', 'damaged_solar_panel']

    # Open the video
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Initialize counters
    counts = {
        'total': 0,
        'clean': 0,
        'dusty': 0,
        'damaged': 0
    }

    # Panel tracker to avoid double counting
    # Using panel centroids as unique identifiers
    panel_tracker = {}  # Maps panel_id -> panel_class

    # Grid tracker
    grid = {}  # Maps "row,col" -> panel_type (0: clean, 1: dusty, 2: damaged)

    # Process one frame per second
    frame_count = 0
    second_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process one frame per second
        if frame_count % int(fps) == 0:
            print(f"Processing frame {frame_count} (second {second_count})")

            # Detect objects in the frame
            results = model(frame)

            # Extract detections
            for result in results:
                boxes = result.boxes.xyxy.cpu().numpy()
                confs = result.boxes.conf.cpu().numpy()
                cls_ids = result.boxes.cls.cpu().numpy().astype(int)

                for box, conf, cls_id in zip(boxes, confs, cls_ids):
                    if conf < 0.5:  # Confidence threshold
                        continue

                    # Extract bounding box coordinates
                    x1, y1, x2, y2 = map(int, box)
                    centroid = ((x1 + x2) // 2, (y1 + y2) // 2)
                    panel_class = class_names[cls_id]

                    # Draw bounding box and label
                    color = (0, 255, 0) if cls_id == 0 else (0, 165, 255) if cls_id == 1 else (0, 0, 255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f"{panel_class} {conf:.2f}",
                                (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                    # Map centroid to grid position
                    grid_row = int(centroid[1] / frame.shape[0] * solar_rows)
                    grid_col = int(centroid[0] / frame.shape[1] * solar_columns)
                    grid_row = min(grid_row, solar_rows - 1)
                    grid_col = min(grid_col, solar_columns - 1)
                    grid_pos = f"{grid_row},{grid_col}"

                    # Create unique panel ID based on grid position and size
                    panel_width = x2 - x1
                    panel_height = y2 - y1
                    panel_id = f"{grid_row}_{grid_col}_{panel_width // 10}_{panel_height // 10}"

                    # Update panel tracker if this is a new panel
                    if panel_id not in panel_tracker:
                        panel_tracker[panel_id] = panel_class
                        counts['total'] += 1

                        if panel_class == 'clean_solar_panel':
                            counts['clean'] += 1
                            grid[grid_pos] = 0
                        elif panel_class == 'dusty_solar_panel':
                            counts['dusty'] += 1
                            grid[grid_pos] = 1
                        elif panel_class == 'damaged_solar_panel':
                            counts['damaged'] += 1
                            grid[grid_pos] = 2

            # Save processed frame based on folder type
            frame_filename = f"frame_{second_count:04d}.jpg"

            # Save a copy to each folder where detections of that type exist
            has_clean = any(cls == 'clean_solar_panel' for cls in panel_tracker.values())
            has_dusty = any(cls == 'dusty_solar_panel' for cls in panel_tracker.values())
            has_damaged = any(cls == 'damaged_solar_panel' for cls in panel_tracker.values())

            if has_clean:
                image_path = os.path.join(clean_folder, frame_filename)
                cv2.imwrite(image_path, frame)
                missionImageData = {
                    'mission_video_id': mission_video_id,
                    'image_path': image_path,
                    'solar_row':grid_row,
                    'solar_col':grid_col,
                    'label':'clean_solar_panel'
                }
                MissionPlannerController.insert_mission_data_image(missionImageData)
            if has_dusty:
                image_path = os.path.join(dusty_folder, frame_filename)
                cv2.imwrite(image_path, frame)
                missionImageData = {
                    'mission_video_id': mission_video_id,
                    'image_path': image_path,
                    'solar_row': grid_row,
                    'solar_col': grid_col,
                    'label': 'dusty_solar_panel'
                }
                MissionPlannerController.insert_mission_data_image(missionImageData)
            if has_damaged:
                image_path = os.path.join(damaged_folder, frame_filename)
                cv2.imwrite(image_path, frame)
                missionImageData = {
                    'mission_video_id': mission_video_id,
                    'image_path': image_path,
                    'solar_row': grid_row,
                    'solar_col': grid_col,
                    'label': 'damaged_solar_panel'
                }
                MissionPlannerController.insert_mission_data_image(missionImageData)

            second_count += 1

        frame_count += 1

    cap.release()

    print(f"Video processing complete. Total panels: {counts['total']}")

    return counts, grid


def make_mission_dirs(data):
    """
    Create directories for mission data if they don't exist.

    Args:
        data: Dictionary containing mission_planner_id

    Returns:
        Tuple of paths: (video_folder, clean_folder, dusty_folder, damaged_folder)
    """
    mission_planner_id = data.get('mission_planner_id')
    base_dir = os.path.join(os.getcwd(), 'uploads', 'missions', str(mission_planner_id))

    # Create main directories
    video_folder = os.path.join(base_dir, 'videos')
    clean_folder = os.path.join(base_dir, 'clean_panels')
    dusty_folder = os.path.join(base_dir, 'dusty_panels')
    damaged_folder = os.path.join(base_dir, 'damaged_panels')

    # Create directories if they don't exist
    for folder in [video_folder, clean_folder, dusty_folder, damaged_folder]:
        os.makedirs(folder, exist_ok=True)

    return video_folder, clean_folder, dusty_folder, damaged_folder
# from ultralytics import YOLO
# import cv2, math, os, json
# from collections import defaultdict
# from pathlib import Path
#
# LABELS = {0: "clean", 1: "dusty", 2: "damaged"}  # class-id → name
#
# def track_video(video_path, out_dirs, rows, cols, model_path,
#                 fps_sample=1, tracker_cfg="bytetrack.yaml"):
#     """
#     Run YOLOv8+ByteTrack on a video and return counts + grid map.
#     out_dirs  : {"clean": Path, "dusty": Path, "damaged": Path}
#     rows/cols : hard-coded solar-array grid size
#     """
#     model = YOLO(model_path)
#     cap = cv2.VideoCapture(video_path)
#     native_fps = cap.get(cv2.CAP_PROP_FPS) or 30
#     gap = max(1, int(native_fps // fps_sample))
#
#     counts = defaultdict(int)          # aggregated counts
#     seen_ids = {}                      # id ➜ label (first label wins)
#     grid_map = {}                      # "r,c" ➜ label
#     frame_idx = 0
#     h = w = None                       # grab once for grid math
#
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         if frame_idx % gap:
#             frame_idx += 1
#             continue
#
#         if h is None:
#             h, w = frame.shape[:2]
#             cell_h, cell_w = h / rows, w / cols
#
#         res = model.track(frame,
#                           persist=True,
#                           verbose=False,
#                           tracker=tracker_cfg)[0]
#
#         # loop detections
#         for box, cls_id, track_id in zip(res.boxes.xyxy.cpu(),
#                                          res.boxes.cls.cpu().tolist(),
#                                          res.boxes.id.cpu().tolist()):
#             label = LABELS[int(cls_id)]
#             # unique-ID counting
#             if track_id not in seen_ids:
#                 seen_ids[track_id] = label
#                 counts[label]      += 1
#                 counts["total"]    += 1
#
#             # grid mapping (use mid-point of box)
#             x_mid = (box[0] + box[2]) / 2
#             y_mid = (box[1] + box[3]) / 2
#             r, c = int(y_mid // cell_h), int(x_mid // cell_w)
#             grid_map[f"{r},{c}"] = label
#
#         # save annotated frame to the class folder of *majority* label
#         majority = max(set(seen_ids.values()), key=list(seen_ids.values()).count)
#         out_path = out_dirs[majority] / f"f{frame_idx}.jpg"
#         cv2.imwrite(str(out_path), res.plot())
#         frame_idx += 1
#
#     cap.release()
#     return dict(counts), grid_map

#Version 2
# from ultralytics import YOLO
# import cv2, random, os, math, json
#
#
# def sample_frames(video_path, fps_sample=1):
#     cap = cv2.VideoCapture(video_path)
#     vfps = cap.get(cv2.CAP_PROP_FPS) or 30
#     frame_gap = int(vfps // fps_sample)
#     frame_idx, samples = 0, []
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         if frame_idx % frame_gap == 0:
#             samples.append((frame_idx, frame.copy()))
#         frame_idx += 1
#     cap.release()
#     return samples  # [(idx, np.ndarray), …]
#
#
# def detect_and_save(samples, model, out_dirs, grid_rows, grid_cols):
#     counts = {"clean": 0, "dusty": 0, "damaged": 0, "total": 0}
#     grid_map = {}  # "r,c": label
#     h, w = samples[0][1].shape[:2]
#     cell_h, cell_w = h / grid_rows, w / grid_cols
#
#     for idx, frame in samples:
#         res = model.predict(source=frame, verbose=False)[0]
#         plotted = res.plot()  # draws bboxes with labels
#         for box, cls in zip(res.boxes.xyxy, res.names):
#             label = cls.split("_solar_panel")[0]  # "clean|dusty|damaged"
#             counts[label] += 1;
#             counts["total"] += 1
#             xmid, ymid = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
#             r, c = int(ymid // cell_h), int(xmid // cell_w)
#             grid_map[f"{r},{c}"] = label
#         # pick folder by majority label in this frame (or loop boxes)
#         frame_out = out_dirs[label] / f"f{idx}.jpg"
#         cv2.imwrite(str(frame_out), plotted)
#     return counts, grid_map


# Version 1
# import os, random, cv2
# from collections import defaultdict
# from ultralytics import YOLO          # pip install ultralytics
#
# # Text labels by class index
# LABELS = {0: "clean", 1: "dusty", 2: "damaged"}
# # Drawing colours (B, G, R)
# CLRS   = {0: (0, 255, 0), 1: (0, 200, 255), 2: (0, 0, 255)}
#
# def sample_random_frames(path: str):
#     """Yield (sec_idx, frame_img) — one random frame per second."""
#     cap = cv2.VideoCapture(path)
#     fps = cap.get(cv2.CAP_PROP_FPS) or 30        # fallback if tag missing
#     total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     seconds = int(total // fps)
#     for sec in range(seconds):
#         start = int(sec * fps)
#         end   = min(int((sec + 1) * fps) - 1, total - 1)
#         cap.set(cv2.CAP_PROP_POS_FRAMES, random.randint(start, end))
#         ok, frame = cap.read()
#         if ok:
#             yield sec, frame
#     cap.release()
#
# def map_to_grid(xyxy, img_w, img_h, rows, cols):
#     """Return (row, col) for bbox centre."""
#     x1, y1, x2, y2 = xyxy
#     cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
#     return int(cy // (img_h / rows)), int(cx // (img_w / cols))
#
# def process_video(video_path, clean_dir, dusty_dir, dam_dir,
#                   rows, cols, model_path):
#     """Run YOLOv8 on 1 fps samples, save annotated frames, return stats."""
#     model = YOLO(model_path)
#     counts = defaultdict(int)          # {'total':…, 'clean':…, …}
#     grid_status = {}                   # {(r,c): "clean"/"dusty"/"damaged"}
#
#     for sec, frame in sample_random_frames(video_path):
#         results = model(frame, verbose=False)[0]
#         if not results.boxes:          # no detections in this frame
#             continue
#
#         h, w = frame.shape[:2]
#         for box in results.boxes:
#             cls   = int(box.cls.item())        # 0 / 1 / 2
#             label = LABELS[cls]
#             color = CLRS[cls]
#
#             counts["total"] += 1
#             counts[label]   += 1
#
#             r, c = map_to_grid(box.xyxy[0].cpu(), w, h, rows, cols)
#             grid_status[(r, c)] = label
#
#             # draw bbox + label
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
#             cv2.putText(frame, label, (x1, max(y1 - 5, 10)),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
#
#         # pick save-folder by majority class in this frame
#         maj_cls = max(results.boxes.cls.tolist())
#         target  = {0: clean_dir, 1: dusty_dir, 2: dam_dir}[maj_cls]
#         os.makedirs(target, exist_ok=True)
#         cv2.imwrite(os.path.join(target, f"f{sec:05}.jpg"), frame)
#
#     # make everything JSON-serialisable
#     return dict(counts), {
#         f"{r},{c}": status for (r, c), status in grid_status.items()
#     }
