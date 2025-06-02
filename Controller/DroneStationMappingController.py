from config import db
from Model import DroneStationMapping,Station,Drone
from .StationController import StationController

class DroneStationMappingController():
    @staticmethod
    def insert_drone_sation_mapping(data):
        try:
            station = Station.query.filter_by(id=data['station_id'],validity=1).first()
            drone = Drone.query.filter_by(id=data['drone_id'],validity=1).first()
            if drone and station:
                StationController.increment_number_of_drones(data['station_id'])
                db.session.commit()
                drone_station_mapping = DroneStationMapping(station_id=data['station_id'],drone_id=data['drone_id'],status=data['status'])
                db.session.add(drone_station_mapping)
                db.session.commit()
                return {
                    "id":drone_station_mapping.id,
                    "drone_id":drone_station_mapping.drone_id,
                    "station_id":drone_station_mapping.station_id,
                    "status":drone_station_mapping.status
                }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def update_drone_station_mapping(data):
        try:
            station = Station.query.filter_by(id=data.get('station_id'), validity=1).first()
            if station is None:
                return {}
            drone_station_mapping = DroneStationMapping.query.filter_by(id=data['id'], validity=1).first()
            if drone_station_mapping:
                StationController.decrement_number_of_drones(drone_station_mapping.station_id)
                drone_station_mapping.station_id = data.get('station_id', drone_station_mapping.station_id)
                drone_station_mapping.drone_id = data.get('drone_id', drone_station_mapping.drone_id)
                db.session.commit()
                StationController.increment_number_of_drones(drone_station_mapping.station_id)
                return {
                    "id": drone_station_mapping.id,
                    "drone_id": drone_station_mapping.drone_id,
                    "station_id": drone_station_mapping.station_id,
                    "status": drone_station_mapping.status
                }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def get_drone_station_mapping_by_id(id):
        try:
            drone_station_mapping = DroneStationMapping.query.filter_by(id=id,validity=1).first()
            if drone_station_mapping:
                return {'id':drone_station_mapping.id,
                        'drone_id':drone_station_mapping.drone_id,
                        'station_id':drone_station_mapping.station_id,
                        'status':drone_station_mapping.status}
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def get_all_drone_station_mappings():
        try:
            drone_station_mappings = DroneStationMapping.query.filter_by(validity=1).all()
            if drone_station_mappings:
                return [{'id':d.id,'drone_id':d.drone_id,'station_id':d.station_id,'status':d.status} for d in drone_station_mappings]
            else:
                return []
        except Exception as e:
            print(e)
            return []
    @staticmethod
    def delete_drone_station_mapping_by_id(id):
        try:
            drone_station_mapping = DroneStationMapping.query.filter_by(id=id,validity=1).first()
            station = Station.query.filter_by(id=drone_station_mapping.station_id,validity=1).first()
            if station:
                StationController.decrement_number_of_drones(station.id)
                db.session.commit()
            if drone_station_mapping:
                drone_station_mapping.validity = 0
                db.session.commit()
                return {'id':drone_station_mapping.id,'drone_id':drone_station_mapping.drone_id,'station_id':drone_station_mapping.station_id,'status':drone_station_mapping.status}
            else:
                return {}
        except Exception as e:
            print(e)
            return {}
