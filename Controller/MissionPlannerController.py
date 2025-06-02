from Controller import SortieController,DroneAvailabilityLogController
from Directories import make_mission_dirs
from config import db
from Model import MissionPlanner, Sortie, Drone, DroneAvailabilityLog, MissionVideo,Route,MissionDataImages
import os
from ProcessSolarVideos import process_video
from ultralytics import YOLO
from pathlib import Path

class MissionPlannerController():
    @staticmethod
    def insert_mission_plan(data):
        try:
            mission_plan = MissionPlanner(
                name=data.get('name'),
                drone_id=data.get('drone_id'),
                route_id=data.get('route_id'),
                start_date=data.get('start_date'),
                start_time=data.get('start_time'),
                status=data.get('status')
            )

            db.session.add(mission_plan)
            db.session.commit()
            data['mission_planner_id'] = mission_plan.id
            drone_availability_log = DroneAvailabilityLogController.insert_drone_availability_log(data)
            return {
               "id": mission_plan.id,
               "name": mission_plan.name,
               "drone_id": mission_plan.drone_id,
               "start_date": mission_plan.start_date.strftime('%d-%m-%Y'),
                "start_time": str(mission_plan.start_time.strftime('%I:%M:%S %p')),
               "status": mission_plan.status,
                "drone_availability_log_id":drone_availability_log.get('id')
            }
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def insert_mission_video(data, video):
        try:
            mission = MissionPlanner.query.filter_by(id=data.get('mission_planner_id'), validity=1).first()
            if mission:
                route = Route.query.filter_by(id=mission.route_id, validity=1).first()
                solar_rows = route.rows
                solar_columns = route.columns
                video_path, clean_folder, dusty_folder, damaged_folder = MissionPlannerController.upload_mission_video(
                    mission.id, video)
                mission_video = MissionVideo(mission_planner_id=data.get("mission_planner_id"),
                                             file_path=video_path)
                db.session.add(mission_video)
                db.session.commit()

                # Process the video with the model
                model_path = r"D:\UNIVERSITY PROJECT\uavauto_aina\yolov8n\weights\best.pt"  # adjust path
                counts, grid = process_video(
                    video_path,
                    clean_folder, dusty_folder, damaged_folder,
                    solar_rows, solar_columns,
                    model_path,
                    mission_video.id
                )

                response_payload = {
                    "id": mission_video.id,
                    "video_path": video_path,
                    "counts": counts,
                    "grid": grid
                }
                return response_payload
            return {}
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def upload_mission_video(mission_planner_id, video):
        try:
            video_folder, clean_folder, dusty_folder, damaged_folder = make_mission_dirs(
                {"mission_planner_id": mission_planner_id})
            file = ''
            for filename in os.listdir(video_folder):
                video_file_name = video.filename.replace(" ", "")
                if filename == f"{mission_planner_id}_{video_file_name}":
                    print(f'File {filename} already exists')
                    return os.path.join(video_folder, filename).replace(
                        "\\", "/"), clean_folder, dusty_folder, damaged_folder
                if filename.split("_")[0] == str(mission_planner_id):
                    file = filename
            if file:
                os.remove(os.path.join(video_folder, file))
            video_path = os.path.join(video_folder,
                                      f'{mission_planner_id}_{video.filename.replace(" ", "")}')
            video.save(video_path)
            return video_path.replace("\\", "/"), clean_folder, dusty_folder, damaged_folder
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def insert_mission_data_image(data):
        try:
            mission_data_image = MissionDataImages(mission_video_id=data.get('mission_video_id'),image_path=data.get('image_path'),solar_row=data.get('solar_row'),solar_column=data.get('solar_column'),label=data.get('label'))
            db.session.add(mission_data_image)
            db.session.commit()
            return{
                'id':mission_data_image.id,
                'mission_video_id':mission_data_image.mission_video_id,
                'image_path': mission_data_image.image_path,
                'solar_row': mission_data_image.solar_row,
                'solar_col': mission_data_image.solar_col,
                'label':mission_data_image.label
            }
        except Exception as e:
            print(e)
            return {}
    #
    # @staticmethod
    # def insert_mission_video(data,video):
    #     try:
    #         mission = MissionPlanner.query.filter_by(id=data.get('mission_planner_id'),validity=1).first()
    #         if mission:
    #             route = Route.query.filter_by(id=mission.route_id,validity=1).first()
    #             solar_rows = route.rows
    #             solar_columns = route.columns
    #             video_path,clean_folder,dusty_folder,damaged_folder = MissionPlannerController.upload_mission_video(mission.id,video)
    #             mission_video = MissionVideo(mission_planner_id=data.get("mission_planner_id"),file_path=video_path)
    #             db.session.add(mission_video)
    #             db.session.commit()
    #             # Impliment the further logic from here make several functions for the task and accomplish it
    #             model_path = r"D:\UNIVERSITY PROJECT\uavauto_aina\yolov8n\weights\best.pt"  # adjust path
    #             model = YOLO(model_path)
    #
    #             counts, grid = track_video(
    #                 video_path,
    #                 {"clean": Path(clean_folder),
    #                  "dusty": Path(dusty_folder),
    #                  "damaged": Path(damaged_folder)},
    #                 solar_rows, solar_columns,
    #                 model_path
    #             )
    #
    #             # samples = sample_frames(video_path, fps_sample=1)
    #             # out_dirs = {
    #             #     "clean": Path(clean_folder),
    #             #     "dusty": Path(dusty_folder),
    #             #     "damaged": Path(damaged_folder)
    #             # }
    #             # counts, grid = detect_and_save(
    #             #     samples, model, out_dirs,
    #             #     solar_rows, solar_columns
    #             # )
    #
    #             # counts, grid = process_video(
    #             #     video_path,
    #             #     clean_folder, dusty_folder, damaged_folder,
    #             #     solar_rows, solar_columns,
    #             #     model_path
    #             # )
    #             #
    #             response_payload = {
    #                 "id": mission_video.id,
    #                 "video_path": video_path,
    #                 "counts": counts,  # plain dict now
    #                 "grid": grid  # {'0,1': 0, '0,2': 2, ...}
    #             }
    #             return response_payload
    #         return {}
    #     except Exception as e:
    #         print(e)
    #         return {}
    #
    # @staticmethod
    # def upload_mission_video(mission_planner_id,video):
    #     try:
    #         video_folder,clean_folder,dusty_folder,damaged_folder = make_mission_dirs({"mission_planner_id":mission_planner_id})
    #         file = ''
    #         for filename in os.listdir(video_folder):
    #             video_file_name = video.filename.replace(" ", "")
    #             if filename == f"{mission_planner_id}_{video_file_name}":
    #                 print(f'File {filename} already exists')
    #                 return os.path.join(video_folder, filename).replace(
    #                     "\\", "/"),clean_folder,dusty_folder,damaged_folder
    #             if filename.split("_")[0] == str(mission_planner_id):
    #                 file = filename
    #         if file:
    #             os.remove(os.path.join(video_folder, file))
    #         video_path = os.path.join(video_folder,
    #                                   f'{mission_planner_id}_{video.filename.replace(" ", "")}')
    #         video.save(video_path)
    #         return video_path.replace("\\", "/"),clean_folder,dusty_folder,damaged_folder
    #     except Exception as e:
    #         print(e)
    #         return {}

    @staticmethod
    def update_mission_plan_by_id(data):
        try:
            mission_plan = MissionPlanner.query.filter_by(id=data.get('id'),validity=1).first()
            print(mission_plan.drone_id)
            drone_availability_log = DroneAvailabilityLog.query.filter_by(mission_planner_id=mission_plan.id,validity=1).first()
            if mission_plan:
                mission_plan.name = data.get('name',mission_plan.name)
                mission_plan.drone_id = data.get('drone_id',mission_plan.drone_id)
                mission_plan.route_id = data.get('route_id', mission_plan.route_id)
                mission_plan.start_date = data.get('start_date',mission_plan.start_date)
                mission_plan.start_time = data.get('start_time',mission_plan.start_time)
                mission_plan.status = data.get('status',mission_plan.status)
                if drone_availability_log:
                    drone_availability_log.drone_id = data.get('drone_id', drone_availability_log.drone_id)


                db.session.commit()
                return {
                    "id": mission_plan.id,
                    "name": mission_plan.name,
                    "drone_id": mission_plan.drone_id,
                    "start_date": mission_plan.start_date.strftime('%d-%m-%Y'),
                    "start_time": str(mission_plan.start_time.strftime('%I:%M:%S %p')),
                    "status": mission_plan.status,
                }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def delete_mission_plan_by_id(mission_planner_id):
        try:
            mission_plan = MissionPlanner.query.filter_by(id=mission_planner_id, validity=1).first()
            if mission_plan:
                mission_plan.validity = 0
            else:
                return {}

            drone_availability_log = DroneAvailabilityLog.query.filter_by(drone_id=mission_plan.drone_id,validity=1).first()
            if drone_availability_log:
                drone_availability_log.validity = 0


            # Commit all changes to the database in one transaction
            db.session.commit()
            return {
                        "id": mission_plan.id,
                        "name": mission_plan.name,
                        "route_id": mission_plan.route_id,
                        "drone_id": mission_plan.drone_id,
                        "start_date": mission_plan.start_date.strftime('%d-%m-%Y'),
                        "start_time": str(mission_plan.start_time.strftime('%I:%M:%S %p')),
                        "status": mission_plan.status,
                    }
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def get_all_mission_plans():
        try:
            mission_plans = MissionPlanner.query.filter_by(validity=1).all()
            if mission_plans:
                result = []
                for mission_plan in mission_plans:


                    mission_dict = {
                        "id": mission_plan.id,
                        "name": mission_plan.name,
                        "route_id": mission_plan.route_id,
                        "drone_id": mission_plan.drone_id,
                        "start_date": mission_plan.start_date.strftime('%d-%m-%Y'),
                        "start_time": mission_plan.start_time.strftime('%I:%M:%S %p'),
                        "status": mission_plan.status
                    }
                    if mission_plan.status not in ('completed', 'aborted'):
                        result.append(mission_dict)
                return result
            else:
                return []
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def get_mission_plan_by_id(mission_plan_id):
        try:
            mission_plan = MissionPlanner.query.filter_by(id=mission_plan_id, validity=1).first()
            if mission_plan:
                return {
                    "id": mission_plan.id,
                    "name": mission_plan.name,
                    "route_id": mission_plan.route_id,
                    "drone_id": mission_plan.drone_id,
                    "start_date": mission_plan.start_date.strftime('%d-%m-%Y'),
                    "start_time": str(mission_plan.start_time.strftime('%I:%M:%S %p')),
                    "status": mission_plan.status
                }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

