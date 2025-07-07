from moviepy import VideoFileClip
from datetime import datetime, timedelta
import numpy
from flask import url_for, send_file

from Controller import SortieController, DroneAvailabilityLogController, DroneController, RouteController,MissionPanelMapController,EfficiencyReportController
from config import db
from Model import MissionPlanner,Sortie, Drone,DroneAvailabilityLog,MissionVideo,Route,MissionDataImages
import os
from ProcessSolarVideos import  process_video
from Directories import  make_mission_dirs

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
                "route_id":mission_plan.route_id,
               "start_date": mission_plan.start_date.strftime('%d-%m-%Y'),
                "start_time": str(mission_plan.start_time.strftime('%I:%M:%S %p')),
               "status": mission_plan.status,
                "drone_availability_log_id":drone_availability_log.get('id')
            }
        except Exception as e:
            print(e)
            return {}

        # Aina code ab run karain
    @staticmethod
    def abort_mission(id):
        try:
            mission_plan = MissionPlanner.query.filter_by(id=id, validity=1).first()
            # print(mission_plan)
            drone_availability_log = DroneAvailabilityLog.query.filter_by(mission_planner_id=mission_plan.id,
                                                                          validity=1).first()
            if drone_availability_log:
                drone_availability_log.validity = 0
            if mission_plan:
                mission_plan.status = 'aborted'
                db.session.commit()
                return {
                    "id": mission_plan.id,
                    "status": mission_plan.status,
                }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

        # Aina Code end
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
            mission_plans = MissionPlanner.query.filter_by(status="pending",validity=1).all()
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

    @staticmethod
    def insert_mission_video(data, video):
        try:
            mission = MissionPlanner.query.filter_by(id=data.get('mission_planner_id'), validity=1).first()
            if mission:
                print('this is mission.id')
                print(mission.id)
                print('this is mission.route id')
                print(mission.route_id)
                print('this is mission.drone id')
                print(mission.drone_id)
                route = Route.query.filter_by(id=mission.route_id, validity=1).first()
                print('this is route.id')
                print(route.id)
                print(f'these are rows and cols {route.rows}, {route.rows}')
                solar_rows = route.rows
                solar_columns = route.columns
                video_path, clean_folder, dusty_folder, damaged_folder = MissionPlannerController.upload_mission_video(
                    mission.id, video
                )

                # Create mission video entry (with default values)
                mission_video = MissionVideo(
                    mission_planner_id=data.get("mission_planner_id"),
                    file_path=video_path,
                    clean_solar_panels=0,
                    dusty_solar_panels=0,
                    damaged_solar_panels=0,
                    total_solar_panels=0
                )

                db.session.add(mission_video)
                db.session.commit()

                mpms = MissionPanelMapController.get_mission_panel_maps_by_mission_id(data.get("mission_planner_id"))

                # framesToKeep = [0, 146, 287, 372, 452, 578] # for wahab's video
                framesToKeep = [51, 144, 224, 294, 365, 493, 612, 763, 1005, 1105, 1187, 1246]  # for aina's video
                # Process the video and get detection results
                model_path = r"D:\UNIVERSITY PROJECT\UAV-AUTO-BACKEND-WEB\yolo11x_solar\weights\best.pt"
                # model_path = r"E:\user\abdul wahab\PythonProjects\final_year_project_backend_v2\yolov8n\weights\best.pt"
                counts, grid = process_video(
                    video_path,
                    clean_folder, dusty_folder, damaged_folder,
                    mpms,
                    model_path,
                    mission_video.id,  # Now we have the ID
                    MissionPlannerController.insert_mission_data_image
                )

                # ✅ Update the same mission_video instance
                mission_video.clean_solar_panels = counts.get('clean', 0)
                mission_video.dusty_solar_panels = counts.get('dusty', 0)
                mission_video.damaged_solar_panels = counts.get('damaged', 0)
                mission_video.total_solar_panels = counts.get('total', 0)

                db.session.commit()  # Save updated values

                # Update mission planner status to completed
                MissionPlannerController.update_mission_plan_by_id({
                    'id': data.get('mission_planner_id'),
                    'status': 'completed'
                })

                for g in grid:
                    g['mission_panel_map_id'] = g['id']
                    EfficiencyReportController.insert_efficiency_report(g)


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
                'solar_column': mission_data_image.solar_column,
                'label':mission_data_image.label
            }
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def get_mission_data_images(data):
        try:
            if data['label'] == "total_solar_panel":
                mission_data_images = MissionDataImages.query.filter_by(mission_video_id=data['id'],validity=1)
            else:
                mission_data_images = MissionDataImages.query.filter_by(mission_video_id=data['id'],label=data['label'],validity=1)


            return [{"id":mission_data_image.id,"mission_video_id":mission_data_image.mission_video_id,
                     "image_path":mission_data_image.image_path,"solar_row":mission_data_image.solar_row,
                     "solar_column":mission_data_image.solar_column,"label":mission_data_image.label,
                     "id":mission_data_image.id,"id":mission_data_image.id} for mission_data_image in mission_data_images]
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def get_mission_data_images2(id):
        try:

            # Changes By AINA (i am getting mission_data_images on the basis of missionPlanner id)
            mv = MissionVideo.query.filter_by(mission_planner_id=id, validity=1).first()
            mission_data_images = MissionDataImages.query.filter_by(mission_video_id=mv.id, validity=1)

            return [{"id": mission_data_image.id, "mission_video_id": mission_data_image.mission_video_id,
                     "image_path": mission_data_image.image_path, "solar_row": mission_data_image.solar_row,
                     "solar_column": mission_data_image.solar_column, "label": mission_data_image.label,
                     "id": mission_data_image.id, "id": mission_data_image.id} for mission_data_image in
                    mission_data_images]
        except Exception as e:
            print(e)
            return {}


    @staticmethod
    def get_all_history():
        try:
            mission_plans = MissionPlanner.query.filter_by(validity=1).all()
            if mission_plans:
                result = []
                for mission_plan in mission_plans:
                    mission_dict = {
                        "id": mission_plan.id,
                        "name": mission_plan.name,
                        "status": mission_plan.status
                    }
                    if mission_plan.status in ('completed', 'aborted'):
                        result.append(mission_dict)
                return result
            else:
                return []
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def get_history_by_id(mission_plan_id):
        try:
            mp = MissionPlanner.query.filter_by(id=mission_plan_id, validity=1).first()
            if mp:
                if mp.status in ('completed', 'aborted'):
                    drone = DroneController.get_drone_by_id(drone_id=mp.drone_id)
                    route = RouteController.get_route_by_id(id=mp.route_id)

                    missionVideo = MissionVideo.query.filter_by(mission_planner_id=mission_plan_id, validity=1).first()



                    mission_dict = {
                        "id": mp.id,
                        "name": mp.name,
                        "drone": drone['name'],
                        "route": route['name'],
                        "start_date": mp.start_date.strftime('%d-%m-%Y'),
                        "start_time": mp.start_time.strftime('%I:%M:%S %p'),
                        "status": mp.status,
                        "mission_video_id":missionVideo.id,
                        "video_url": missionVideo.file_path,
                        "clean": missionVideo.clean_solar_panels,
                        "dusty": missionVideo.dusty_solar_panels,
                        "damaged": missionVideo.damaged_solar_panels
                    }
                    return mission_dict
            else:
                return []
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def get_video_path(mission_planner_id):
        missionVideo = MissionVideo.query.filter_by(mission_planner_id=mission_planner_id, validity=1).first()
        if not missionVideo:
            return None
        return missionVideo.file_path


    @staticmethod
    def stream_video(mission_id):

        mp = MissionPlanner.query.filter_by(id=mission_id, validity=1).first()
        if not mp or mp.status not in ('completed', 'aborted'):
            raise ValueError("Mission not available")

        path = MissionPlannerController.get_video_path(mission_id)

        return send_file(
            path,
            mimetype='video/mp4',
            as_attachment=False,
            conditional=True
        )

    @classmethod
    def get_duration_and_end_date(mission_planner_id):
        mission = MissionPlanner.query.get(mission_planner_id)
        if not mission:
            raise ValueError("MissionPlanner not found")

        video_folder, _, _, _ = make_mission_dirs({"mission_planner_id": mission_planner_id})
        video_file = None
        for fn in os.listdir(video_folder):
            if fn.startswith(f"{mission_planner_id}_"):
                video_file = fn
                break
        if not video_file:
            raise FileNotFoundError(f"No video found for mission {mission_planner_id} in {video_folder}")

        video_path = os.path.join(video_folder, video_file)

        clip = VideoFileClip(video_path)
        dur_seconds = clip.duration
        clip.close()

        start_dt = datetime.combine(mission.start_date, mission.start_time)
        end_dt = start_dt + timedelta(seconds=dur_seconds)

        end_date = end_dt.date()
        end_time = end_dt.time()

        return dur_seconds, end_date, end_time



# from moviepy import VideoFileClip
# from datetime import datetime, timedelta
# import numpy
# from flask import url_for, send_file
#
# from Controller import SortieController, DroneAvailabilityLogController, DroneController, RouteController
# from config import db
# from Model import MissionPlanner,Sortie, Drone,DroneAvailabilityLog,MissionVideo,Route,MissionDataImages
# import os
# from ProcessSolarVideos import  process_video
# from Directories import  make_mission_dirs
#
# class MissionPlannerController():
#     @staticmethod
#     def insert_mission_plan(data):
#         try:
#             mission_plan = MissionPlanner(
#                 name=data.get('name'),
#                 drone_id=data.get('drone_id'),
#                 route_id=data.get('route_id'),
#                 start_date=data.get('start_date'),
#                 start_time=data.get('start_time'),
#                 status=data.get('status')
#             )
#
#             db.session.add(mission_plan)
#             db.session.commit()
#             data['mission_planner_id'] = mission_plan.id
#             drone_availability_log = DroneAvailabilityLogController.insert_drone_availability_log(data)
#             return {
#                "id": mission_plan.id,
#                "name": mission_plan.name,
#                "drone_id": mission_plan.drone_id,
#                 "route_id":mission_plan.route_id,
#                "start_date": mission_plan.start_date.strftime('%d-%m-%Y'),
#                 "start_time": str(mission_plan.start_time.strftime('%I:%M:%S %p')),
#                "status": mission_plan.status,
#                 "drone_availability_log_id":drone_availability_log.get('id')
#             }
#         except Exception as e:
#             print(e)
#             return {}
#
#
#     @staticmethod
#     def update_mission_plan_by_id(data):
#         try:
#             mission_plan = MissionPlanner.query.filter_by(id=data.get('id'),validity=1).first()
#             print(mission_plan.drone_id)
#             drone_availability_log = DroneAvailabilityLog.query.filter_by(mission_planner_id=mission_plan.id,validity=1).first()
#             if mission_plan:
#                 mission_plan.name = data.get('name',mission_plan.name)
#                 mission_plan.drone_id = data.get('drone_id',mission_plan.drone_id)
#                 mission_plan.route_id = data.get('route_id', mission_plan.route_id)
#                 mission_plan.start_date = data.get('start_date',mission_plan.start_date)
#                 mission_plan.start_time = data.get('start_time',mission_plan.start_time)
#                 mission_plan.status = data.get('status',mission_plan.status)
#                 if drone_availability_log:
#                     drone_availability_log.drone_id = data.get('drone_id', drone_availability_log.drone_id)
#
#
#                 db.session.commit()
#                 return {
#                     "id": mission_plan.id,
#                     "name": mission_plan.name,
#                     "drone_id": mission_plan.drone_id,
#                     "start_date": mission_plan.start_date.strftime('%d-%m-%Y'),
#                     "start_time": str(mission_plan.start_time.strftime('%I:%M:%S %p')),
#                     "status": mission_plan.status,
#                 }
#             else:
#                 return {}
#         except Exception as e:
#             print(e)
#             return {}
#
#     @staticmethod
#     def delete_mission_plan_by_id(mission_planner_id):
#         try:
#             mission_plan = MissionPlanner.query.filter_by(id=mission_planner_id, validity=1).first()
#             if mission_plan:
#                 mission_plan.validity = 0
#             else:
#                 return {}
#
#             drone_availability_log = DroneAvailabilityLog.query.filter_by(drone_id=mission_plan.drone_id,validity=1).first()
#             if drone_availability_log:
#                 drone_availability_log.validity = 0
#
#
#             # Commit all changes to the database in one transaction
#             db.session.commit()
#             return {
#                         "id": mission_plan.id,
#                         "name": mission_plan.name,
#                         "route_id": mission_plan.route_id,
#                         "drone_id": mission_plan.drone_id,
#                         "start_date": mission_plan.start_date.strftime('%d-%m-%Y'),
#                         "start_time": str(mission_plan.start_time.strftime('%I:%M:%S %p')),
#                         "status": mission_plan.status,
#                     }
#         except Exception as e:
#             print(e)
#             return {}
#
#     @staticmethod
#     def get_all_mission_plans():
#         try:
#             mission_plans = MissionPlanner.query.filter_by(status="pending",validity=1).all()
#             if mission_plans:
#                 result = []
#                 for mission_plan in mission_plans:
#
#                     mission_dict = {
#                         "id": mission_plan.id,
#                         "name": mission_plan.name,
#                         "route_id": mission_plan.route_id,
#                         "drone_id": mission_plan.drone_id,
#                         "start_date": mission_plan.start_date.strftime('%d-%m-%Y'),
#                         "start_time": mission_plan.start_time.strftime('%I:%M:%S %p'),
#                         "status": mission_plan.status
#                     }
#                     if mission_plan.status not in ('completed', 'aborted'):
#                         result.append(mission_dict)
#                 return result
#             else:
#                 return []
#         except Exception as e:
#             print(e)
#             return []
#
#     @staticmethod
#     def get_mission_plan_by_id(mission_plan_id):
#         try:
#             mission_plan = MissionPlanner.query.filter_by(id=mission_plan_id, validity=1).first()
#             if mission_plan:
#                 return {
#                     "id": mission_plan.id,
#                     "name": mission_plan.name,
#                     "route_id": mission_plan.route_id,
#                     "drone_id": mission_plan.drone_id,
#                     "start_date": mission_plan.start_date.strftime('%d-%m-%Y'),
#                     "start_time": str(mission_plan.start_time.strftime('%I:%M:%S %p')),
#                     "status": mission_plan.status
#                 }
#             else:
#                 return {}
#         except Exception as e:
#             print(e)
#             return {}
#
#     @staticmethod
#     def insert_mission_video(data, video):
#         try:
#             mission = MissionPlanner.query.filter_by(id=data.get('mission_planner_id'), validity=1).first()
#             if mission:
#                 print('this is mission.id')
#                 print(mission.id)
#                 print('this is mission.route id')
#                 print(mission.route_id)
#                 print('this is mission.drone id')
#                 print(mission.drone_id)
#                 route = Route.query.filter_by(id=mission.route_id, validity=1).first()
#                 print('this is route.id')
#                 print(route.id)
#                 print(f'these are rows and cols {route.rows}, {route.rows}')
#                 solar_rows = route.rows
#                 solar_columns = route.columns
#                 video_path, clean_folder, dusty_folder, damaged_folder = MissionPlannerController.upload_mission_video(
#                     mission.id, video
#                 )
#
#                 # Create mission video entry (with default values)
#                 mission_video = MissionVideo(
#                     mission_planner_id=data.get("mission_planner_id"),
#                     file_path=video_path,
#                     clean_solar_panels=0,
#                     dusty_solar_panels=0,
#                     damaged_solar_panels=0,
#                     total_solar_panels=0
#                 )
#
#                 db.session.add(mission_video)
#                 db.session.commit()
#                 # framesToKeep = [0, 146, 287, 372, 452, 578] # for wahab's video
#                 framesToKeep = [51, 144, 224, 294, 365, 493, 612, 763, 1005, 1105, 1187, 1246]  # for aina's video
#                 # Process the video and get detection results
#                 model_path = r"E:\user\abdul wahab\PythonProjects\final_year_project_backend_v2\yolo11x_solar\weights\best.pt"
#                 # model_path = r"E:\user\abdul wahab\PythonProjects\final_year_project_backend_v2\yolov8n\weights\best.pt"
#                 counts, grid = process_video(
#                     video_path,
#                     clean_folder, dusty_folder, damaged_folder,
#                     solar_rows, solar_columns,
#                     model_path,
#                     mission_video.id,  # Now we have the ID
#                     framesToKeep,
#                     MissionPlannerController.insert_mission_data_image
#                 )
#
#                 # ✅ Update the same mission_video instance
#                 mission_video.clean_solar_panels = counts.get('clean', 0)
#                 mission_video.dusty_solar_panels = counts.get('dusty', 0)
#                 mission_video.damaged_solar_panels = counts.get('damaged', 0)
#                 mission_video.total_solar_panels = counts.get('total', 0)
#
#                 db.session.commit()  # Save updated values
#
#                 # Update mission planner status to completed
#                 MissionPlannerController.update_mission_plan_by_id({
#                     'id': data.get('mission_planner_id'),
#                     'status': 'completed'
#                 })
#
#                 response_payload = {
#                     "id": mission_video.id,
#                     "video_path": video_path,
#                     "counts": counts,
#                     "grid": grid
#                 }
#                 return response_payload
#
#             return {}
#         except Exception as e:
#             print(e)
#             return {}
#     @staticmethod
#     def upload_mission_video(mission_planner_id, video):
#         try:
#             video_folder, clean_folder, dusty_folder, damaged_folder = make_mission_dirs(
#                 {"mission_planner_id": mission_planner_id})
#             file = ''
#             for filename in os.listdir(video_folder):
#                 video_file_name = video.filename.replace(" ", "")
#                 if filename == f"{mission_planner_id}_{video_file_name}":
#                     print(f'File {filename} already exists')
#                     return os.path.join(video_folder, filename).replace(
#                         "\\", "/"), clean_folder, dusty_folder, damaged_folder
#                 if filename.split("_")[0] == str(mission_planner_id):
#                     file = filename
#             if file:
#                 os.remove(os.path.join(video_folder, file))
#             video_path = os.path.join(video_folder,
#                                       f'{mission_planner_id}_{video.filename.replace(" ", "")}')
#             video.save(video_path)
#             return video_path.replace("\\", "/"), clean_folder, dusty_folder, damaged_folder
#         except Exception as e:
#             print(e)
#             return {}
#
#     @staticmethod
#     def insert_mission_data_image(data):
#         try:
#             mission_data_image = MissionDataImages(mission_video_id=data.get('mission_video_id'),image_path=data.get('image_path'),solar_row=data.get('solar_row'),solar_column=data.get('solar_column'),label=data.get('label'))
#             db.session.add(mission_data_image)
#             db.session.commit()
#             return{
#                 'id':mission_data_image.id,
#                 'mission_video_id':mission_data_image.mission_video_id,
#                 'image_path': mission_data_image.image_path,
#                 'solar_row': mission_data_image.solar_row,
#                 'solar_column': mission_data_image.solar_column,
#                 'label':mission_data_image.label
#             }
#         except Exception as e:
#             print(e)
#             return {}
#
#     @staticmethod
#     def get_mission_data_images(data):
#         try:
#             if data['label'] == "total_solar_panel":
#                 mission_data_images = MissionDataImages.query.filter_by(mission_video_id=data['id'],validity=1)
#             else:
#                 mission_data_images = MissionDataImages.query.filter_by(mission_video_id=data['id'],label=data['label'],validity=1)
#
#
#             return [{"id":mission_data_image.id,"mission_video_id":mission_data_image.mission_video_id,
#                      "image_path":mission_data_image.image_path,"solar_row":mission_data_image.solar_row,
#                      "solar_column":mission_data_image.solar_column,"label":mission_data_image.label,
#                      "id":mission_data_image.id,"id":mission_data_image.id} for mission_data_image in mission_data_images]
#         except Exception as e:
#             print(e)
#             return {}
#
#     @staticmethod
#     def get_mission_data_images2(id):
#         try:
#
#             # Changes By AINA (i am getting mission_data_images on the basis of missionPlanner id)
#             mv = MissionVideo.query.filter_by(mission_planner_id=id, validity=1).first()
#             mission_data_images = MissionDataImages.query.filter_by(mission_video_id=mv.id, validity=1)
#
#             return [{"id": mission_data_image.id, "mission_video_id": mission_data_image.mission_video_id,
#                      "image_path": mission_data_image.image_path, "solar_row": mission_data_image.solar_row,
#                      "solar_column": mission_data_image.solar_column, "label": mission_data_image.label,
#                      "id": mission_data_image.id, "id": mission_data_image.id} for mission_data_image in
#                     mission_data_images]
#         except Exception as e:
#             print(e)
#             return {}
#
#
#     @staticmethod
#     def get_all_history():
#         try:
#             mission_plans = MissionPlanner.query.filter_by(validity=1).all()
#             if mission_plans:
#                 result = []
#                 for mission_plan in mission_plans:
#                     mission_dict = {
#                         "id": mission_plan.id,
#                         "name": mission_plan.name,
#                         "status": mission_plan.status
#                     }
#                     if mission_plan.status in ('completed', 'aborted'):
#                         result.append(mission_dict)
#                 return result
#             else:
#                 return []
#         except Exception as e:
#             print(e)
#             return []
#
#     @staticmethod
#     def get_history_by_id(mission_plan_id):
#         try:
#             mp = MissionPlanner.query.filter_by(id=mission_plan_id, validity=1).first()
#             if mp:
#                 if mp.status in ('completed', 'aborted'):
#                     drone = DroneController.get_drone_by_id(drone_id=mp.drone_id)
#                     route = RouteController.get_route_by_id(id=mp.route_id)
#
#                     missionVideo = MissionVideo.query.filter_by(mission_planner_id=mission_plan_id, validity=1).first()
#
#
#
#                     mission_dict = {
#                         "id": mp.id,
#                         "name": mp.name,
#                         "drone": drone['name'],
#                         "route": route['name'],
#                         "start_date": mp.start_date.strftime('%d-%m-%Y'),
#                         "start_time": mp.start_time.strftime('%I:%M:%S %p'),
#                         "status": mp.status,
#                         "mission_video_id":missionVideo.id,
#                         "video_url": missionVideo.file_path,
#                         "clean": missionVideo.clean_solar_panels,
#                         "dusty": missionVideo.dusty_solar_panels,
#                         "damaged": missionVideo.damaged_solar_panels
#                     }
#                     return mission_dict
#             else:
#                 return []
#         except Exception as e:
#             print(e)
#             return []
#
#     @staticmethod
#     def get_video_path(mission_planner_id):
#         missionVideo = MissionVideo.query.filter_by(mission_planner_id=mission_planner_id, validity=1).first()
#         if not missionVideo:
#             return None
#         return missionVideo.file_path
#
#
#     @staticmethod
#     def stream_video(mission_id):
#
#         mp = MissionPlanner.query.filter_by(id=mission_id, validity=1).first()
#         if not mp or mp.status not in ('completed', 'aborted'):
#             raise ValueError("Mission not available")
#
#         path = MissionPlannerController.get_video_path(mission_id)
#
#         return send_file(
#             path,
#             mimetype='video/mp4',
#             as_attachment=False,
#             conditional=True
#         )
#
#     @classmethod
#     def get_duration_and_end_date(mission_planner_id):
#         mission = MissionPlanner.query.get(mission_planner_id)
#         if not mission:
#             raise ValueError("MissionPlanner not found")
#
#         video_folder, _, _, _ = make_mission_dirs({"mission_planner_id": mission_planner_id})
#         video_file = None
#         for fn in os.listdir(video_folder):
#             if fn.startswith(f"{mission_planner_id}_"):
#                 video_file = fn
#                 break
#         if not video_file:
#             raise FileNotFoundError(f"No video found for mission {mission_planner_id} in {video_folder}")
#
#         video_path = os.path.join(video_folder, video_file)
#
#         clip = VideoFileClip(video_path)
#         dur_seconds = clip.duration
#         clip.close()
#
#         start_dt = datetime.combine(mission.start_date, mission.start_time)
#         end_dt = start_dt + timedelta(seconds=dur_seconds)
#
#         end_date = end_dt.date()
#         end_time = end_dt.time()
#
#         return dur_seconds, end_date, end_time