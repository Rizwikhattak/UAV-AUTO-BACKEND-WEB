from config import db
from Model import DroneAvailabilityLog,Drone
from datetime import datetime, timedelta

class DroneAvailabilityLogController():
    @staticmethod
    def calculate_datatime_limits(start_date,start_time,time_thresh=3):
        start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M:%S")
        start_time_limit = start_datetime - timedelta(hours=time_thresh)
        end_time_limit = start_datetime + timedelta(hours=time_thresh)
        start_date_limit = start_time_limit.strftime("%Y-%m-%d")
        end_date_limit = end_time_limit.strftime("%Y-%m-%d")
        print("Start Time:", start_datetime.strftime("%H:%M:%S"))
        print("Start Time Limit:", start_time_limit.strftime("%H:%M:%S"))
        print("End Time Limit:", end_time_limit.strftime("%H:%M:%S"))
        print("Start Date Limit:", start_date_limit)
        print("End Date Limit:", end_date_limit)
        return start_time_limit,end_time_limit,start_date_limit,end_date_limit

    @staticmethod
    def insert_drone_availability_log(data):
        try:
            (start_time_limit,
             end_time_limit,
             start_date_limit,
             end_date_limit) = DroneAvailabilityLogController.calculate_datatime_limits(data['start_date'],data['start_time'])
            drone_availability_log = DroneAvailabilityLog(drone_id=data['drone_id'],
                                                          start_date=data['start_date'],
                                                          mission_planner_id = data['mission_planner_id'],
                                                          start_date_limit=start_date_limit,
                                                          start_time_limit=start_time_limit,
                                                          end_date_limit=end_date_limit,
                                                          end_time_limit=end_time_limit)
            db.session.add(drone_availability_log)
            db.session.commit()
            return {
                "id": drone_availability_log.id,
                "drone_id": drone_availability_log.drone_id,
                "mission_planner_id":drone_availability_log.mission_planner_id,
                "start_date": drone_availability_log.start_date.strftime('%d-%m-%Y'),
                "start_date_limit": drone_availability_log.start_date_limit.strftime('%d-%m-%Y'),
                "start_time_limit": str(drone_availability_log.start_time_limit.strftime('%I:%M:%S %p')),
                "end_date_limit": drone_availability_log.end_date_limit.strftime('%d-%m-%Y'),
                "end_time_limit": str(drone_availability_log.end_time_limit.strftime('%I:%M:%S %p'))
            }
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def get_all_drone_availability_logs():
        try:
            drone_availability_logs = DroneAvailabilityLog.query.filter_by(validity=1).all()

            if drone_availability_logs:
                return [{
                "id": drone_availability_log.id,
                "drone_id": drone_availability_log.drone_id,
                "mission_planner_id":drone_availability_log.mission_planner_id,
                "start_date": drone_availability_log.start_date.strftime('%d-%m-%Y'),
                "start_date_limit": drone_availability_log.start_date_limit.strftime('%d-%m-%Y'),
                "start_time_limit": str(drone_availability_log.start_time_limit.strftime('%I:%M:%S %p')),
                "end_date_limit": drone_availability_log.end_date_limit.strftime('%d-%m-%Y'),
                "end_time_limit": str(drone_availability_log.end_time_limit.strftime('%I:%M:%S %p'))
            } for drone_availability_log in drone_availability_logs]
            else:
                return []
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def get_drone_availability_log_by_id(id):
        try:
            drone_availability_log = DroneAvailabilityLog.query.filter_by(id=id,validity=1).first()
            if drone_availability_log:
                return {
                "id": drone_availability_log.id,
                "drone_id": drone_availability_log.drone_id,
                "mission_planner_id":drone_availability_log.mission_planner_id,
                "start_date": drone_availability_log.start_date.strftime('%d-%m-%Y'),
                "start_date_limit": drone_availability_log.start_date_limit.strftime('%d-%m-%Y'),
                "start_time_limit": str(drone_availability_log.start_time_limit.strftime('%I:%M:%S %p')),
                "end_date_limit": drone_availability_log.end_date_limit.strftime('%d-%m-%Y'),
                "end_time_limit": str(drone_availability_log.end_time_limit.strftime('%I:%M:%S %p'))
            }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def update_drone_availability_log_by_id(data):
        try:
            drone_availability_log = DroneAvailabilityLog.query.filter_by(id=data['id'],validity=1).first()
            if drone_availability_log:
                drone_availability_log.start_date = data.get('start_date',drone_availability_log.start_date)
                if data.get('start_date') and data.get('start_time'):
                    (start_time_limit,
                     end_time_limit,
                     start_date_limit,
                     end_date_limit) = DroneAvailabilityLogController.calculate_datatime_limits(data.get('start_date'),
                                                                                            data.get('start_time'))
                    drone_availability_log.start_date_limit = start_date_limit
                    drone_availability_log.start_time_limit = start_time_limit
                    drone_availability_log.end_date_limit = end_date_limit
                    drone_availability_log.end_time_limit = end_time_limit
                if data.get('drone_id'):
                    drone = Drone.query.filter_by(id = data.get('drone_id'),validity=1).first()
                    if drone:
                        drone_availability_log.drone_id = data.get('drone_id',drone_availability_log.drone_id)
                db.session.commit()
                return {
                "id": drone_availability_log.id,
                "drone_id": drone_availability_log.drone_id,
                "mission_planner_id":drone_availability_log.mission_planner_id,
                "start_date": drone_availability_log.start_date.strftime('%d-%m-%Y'),
                "start_date_limit": drone_availability_log.start_date_limit.strftime('%d-%m-%Y'),
                "start_time_limit": str(drone_availability_log.start_time_limit.strftime('%I:%M:%S %p')),
                "end_date_limit": drone_availability_log.end_date_limit.strftime('%d-%m-%Y'),
                "end_time_limit": str(drone_availability_log.end_time_limit.strftime('%I:%M:%S %p'))
                }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def delete_drone_availability_log_by_id(id):
        try:
            drone_availability_log = DroneAvailabilityLog.query.filter_by(id=id,validity=1).first()
            if drone_availability_log:
                drone_availability_log.validity = 0
                db.session.commit()
                return {
                "id": drone_availability_log.id,
                "drone_id": drone_availability_log.drone_id,
                "mission_planner_id":drone_availability_log.mission_planner_id,
                "start_date": drone_availability_log.start_date.strftime('%d-%m-%Y'),
                "start_date_limit": drone_availability_log.start_date_limit.strftime('%d-%m-%Y'),
                "start_time_limit": str(drone_availability_log.start_time_limit.strftime('%I:%M:%S %p')),
                "end_date_limit": drone_availability_log.end_date_limit.strftime('%d-%m-%Y'),
                "end_time_limit": str(drone_availability_log.end_time_limit.strftime('%I:%M:%S %p'))
                }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}



if __name__ == "__main__":
    # Input data
    start_date = "2025-1-14"
    start_time = "01:53:04"
    time_thresh = 3  # Threshold in hours

    # Combine date and time into a single datetime object
    start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M:%S")

    # Calculate time limits
    start_time_limit = start_datetime - timedelta(hours=time_thresh)
    end_time_limit = start_datetime + timedelta(hours=time_thresh)
    start_date_limit = start_time_limit.strftime("%Y-%m-%d")
    end_date_limit = end_time_limit.strftime("%Y-%m-%d")
    # Print the results
    print("Start Time:", start_datetime.strftime("%H:%M:%S"))
    print("Start Time Limit:", start_time_limit.strftime("%H:%M:%S"))
    print("End Time Limit:", end_time_limit.strftime("%H:%M:%S"))
    print("Start Date Limit:", start_date_limit)
    print("End Date Limit:", end_date_limit)


# if __name__ == "__main__":
#     start_date = "2025-1-14"
#     start_time = "01:53:04"
#     start_date_limit = start_date
#     time_thresh = 3
#
#     time_limit_for_start = int(start_time.split(':')[0]) - time_thresh
#     if time_limit_for_start<0:
#         time_limit_for_start = time_limit_for_start + 24
#         date_limit_for_start = int(start_date.split('-')[2])-1
#         if date_limit_for_start<=0:
#             date_limit_for_start = 30
#             start_date_limit = f"{start_date.split('-')[0]}-{int(start_date.split('-')[1])-1}-{date_limit_for_start}"
#         else:
#             start_date_limit = f"{start_date.split('-')[0]}-{start_date.split('-')[1]}-{int(start_date.split('-')[2])-1}"
#     start_time_limit = f"{time_limit_for_start:02d}:{start_time.split(':')[1]}:{start_time.split(':')[2]}"
#
#     time_limit_for_end = int(start_time.split(':')[0]) + time_thresh
#     if time_limit_for_end>=24:
#         time_limit_for_end = time_limit_for_end - 24
#     end_time_limit = f"{time_limit_for_end:02d}:{start_time.split(':')[1]}:{start_time.split(':')[2]}"
#
#     print(start_time)
#     print(start_time_limit)
#     print(end_time_limit)
#     print(time_limit_for_end)
