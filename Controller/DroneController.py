from config import db,app
from Model import Drone,Station,DroneStationMapping
from .DroneStationMappingController import DroneStationMappingController
from .StationController import StationController
import os
class DroneController():
    @staticmethod
    def insert_drone(data,drone_img):
        try:
            station = Station.query.filter_by(id=data['station_id'],validity=1).first()
            if station:
                drone = Drone(name=data['name'],speed=data['speed'],flight_duration=data['flight_duration'],ceiling=data['ceiling'],fps=data['fps'])
                db.session.add(drone)
                db.session.commit()
                if drone_img:
                    image_path = DroneController.upload_drone_image(drone.id,drone_img)
                    drone.image_path = image_path
                    db.session.commit()
                newData = {
                    'station_id':data['station_id'],
                    'drone_id':drone.id,
                    'status':1
                }
                drone_station_mapping = DroneStationMappingController.insert_drone_sation_mapping(newData)
                # update_drone_nums = StationController.increment_number_of_drones(data['station_id'])
                return {
                "id": drone.id,
                "name": drone.name,
                "ceiling": drone.ceiling,
                "flight_duration": drone.flight_duration,
                "fps": drone.fps,
                "speed": drone.speed,
                'station_id':drone_station_mapping['station_id'],
                'status':drone_station_mapping['status'],
                'drone_station_mapping_id':drone_station_mapping['id'],
                "image_path": drone.image_path,
                }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

    #Helper Function
    @staticmethod
    def upload_drone_image(drone_id,drone_img):
        file = ''
        for filename in os.listdir(app.config['DRONE_PROFILE_PICTURES_FOLDER']):
            drone_file_name = drone_img.filename.replace(" ", "")
            if filename == f"{drone_id}_{drone_file_name}":
                print(f'File {filename} already exists')
                return os.path.join(app.config['DRONE_PROFILE_PICTURES_FOLDER'], filename).replace(
                    "\\", "/")
            if filename.split("_")[0] == str(drone_id):
                file = filename
        if file:
            os.remove(os.path.join(app.config['DRONE_PROFILE_PICTURES_FOLDER'], file))
        image_path = os.path.join(app.config['DRONE_PROFILE_PICTURES_FOLDER'], f'{drone_id}_{drone_img.filename.replace(" ", "")}')
        drone_img.save(image_path)
        return image_path.replace("\\", "/")

    @staticmethod
    def delete_drone_by_id(drone_id):
        try:
            drone = Drone.query.filter_by(id=drone_id,validity=1).first()
            if drone:
                drone.validity = 0
                db.session.commit()
                dsm=DroneStationMapping.query.filter_by(drone_id=drone.id, validity=1).first()
                drone_station_mapping = DroneStationMappingController.delete_drone_station_mapping_by_id(dsm.id)
                # StationController.decrement_number_of_drones(drone_station_mapping.get('station_id'))
                return {
                    "id": drone.id,
                    "name": drone.name,
                    "ceiling": drone.ceiling,
                    "flight_duration": drone.flight_duration,
                    "fps": drone.fps,
                    "speed": drone.speed,
                    'station_id': drone_station_mapping['station_id'],
                    'status': drone_station_mapping['status'],
                    'drone_station_mapping_id': drone_station_mapping['id'],
                    "image_path": drone.image_path,
                }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def update_drone_by_id(data, drone_img):
        try:
            drone = Drone.query.filter_by(id=data.get('id'), validity=1).first()
            drone_station_mapping = DroneStationMappingController.get_drone_station_mapping_by_id(data.get('id'))
            # Get the current mapping's station_id if needed
            station = None
            if drone_station_mapping:
                station = Station.query.filter_by(id=drone_station_mapping.get('station_id'), validity=1).first()
                print("Current Station:", station)
            else:
                print("No existing drone-station mapping found.")

            if drone:
                # If there's an existing mapping, decrement the current station's drone count
                if drone_station_mapping and station:
                    StationController.decrement_number_of_drones(station.id)

                # Update the drone's image if a new one is provided
                if drone_img:
                    image_path = DroneController.upload_drone_image(drone.id, drone_img)
                    drone.image_path = image_path

                # Update the drone fields
                drone.name = data.get('name', drone.name)
                drone.speed = float(data.get('speed', drone.speed))
                drone.ceiling = float(data.get('ceiling', drone.ceiling))
                drone.flight_duration = float(data.get('flight_duration', drone.flight_duration))
                drone.fps = int(data.get('fps', drone.fps))
                # Optionally update drone.image_path from data if needed
                db.session.commit()

                # Check if a new station_id is provided in the data
                new_station_id = data.get('station_id')
                if new_station_id is not None and new_station_id != "":
                    # Ensure new_station_id is an integer
                    new_station_id = int(new_station_id)
                    # Update the mapping only if new_station_id is valid
                    DroneStationMappingController.update_drone_station_mapping(drone)
                    # Increment the new station's drone count
                    StationController.increment_number_of_drones(new_station_id)
                else:
                    print("No new station_id provided; skipping mapping update.")

                # Return a dictionary of updated drone data
                return {
                    'id': drone.id,
                    'name': drone.name,
                    'speed': drone.speed,
                    'flight_duration': drone.flight_duration,
                    'ceiling': drone.ceiling,
                    'fps': drone.fps,
                    'image_path': drone.image_path
                }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def get_all_drones():
        try:

            drones = (db.session.query(Drone,DroneStationMapping)
                        .join(DroneStationMapping,Drone.id==DroneStationMapping.drone_id)
                        .filter(Drone.validity==1,DroneStationMapping.validity==1).all())

            if drones:
                return [{'id':d.id,
                         'name':d.name,
                         'speed':d.speed,
                         'flight_duration':d.flight_duration,
                         'ceiling':d.ceiling,
                         'fps':d.fps,
                         'image_path':d.image_path,
                         'station_id':ds.station_id} for d,ds in drones]
            else:
                return []
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def get_drone_by_id(drone_id):
        try:
            drone,drone_station_mapping = (db.session.query(Drone,DroneStationMapping)
                        .join(DroneStationMapping,Drone.id==DroneStationMapping.drone_id)
                        .filter(Drone.validity==1,DroneStationMapping.validity==1,Drone.id==drone_id).first())
            if drone:
                return {'id':drone.id,
                        'name':drone.name,
                        'speed':drone.speed,
                        'flight_duration':drone.flight_duration,
                        'ceiling':drone.ceiling,
                        'fps':drone.fps,
                        'image_path':drone.image_path,
                        "station_id":drone_station_mapping.station_id}
            else:
                return {}
        except Exception as e:
            print(e)
            return {}
