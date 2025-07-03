from config import db
from Model import Sortie

class SortieController():
    @staticmethod
    def insert_sortie(data):
        try:
            sortie=Sortie(mission_planner_id = data['mission_planner_id'],start_date=data['start_date'],end_date=data['end_date'],start_time=data['start_time'],end_time=data['end_time'],duration=data['duration'])
            db.session.add(sortie)
            db.session.commit()

            return {
                "id": sortie.id,
                "mission_planner_id": sortie.mission_planner_id,
                "start_date": sortie.start_date.strftime('%d-%m-%Y'),
                "start_time": str(sortie.start_time.strftime('%I:%M:%S %p')),
                "end_date": sortie.end_date.strftime('%d-%m-%Y'),
                "end_time": str(sortie.end_time.strftime('%I:%M:%S %p')),
                "duration": sortie.duration
            }
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def get_all_sorties():
        try:
            sorties =  Sortie.query.filter_by(validity=1).all()

            if sorties:
                return [{
                    "id": sortie.id,
                    "mission_planner_id": sortie.mission_planner_id,
                    "start_date": sortie.start_date.strftime('%d-%m-%Y'),
                    "start_time": str(sortie.start_time.strftime('%I:%M:%S %p')),
                    "end_date": sortie.end_date.strftime('%d-%m-%Y'),
                    "end_time": str(sortie.end_time.strftime('%I:%M:%S %p')),
                    "duration": sortie.duration
                } for sortie in sorties]
            else:
                return []
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def get_sortie_by_id(id):
        try:
            sortie = Sortie.query.filter_by(id=id,validity=1).first()
            if sortie:

                return {
                    "id": sortie.id,
                    "mission_planner_id": sortie.mission_planner_id,
                    "start_date": sortie.start_date.strftime('%d-%m-%Y'),
                    "start_time": str(sortie.start_time.strftime('%I:%M:%S %p')),
                    "end_date": sortie.end_date.strftime('%d-%m-%Y'),
                    "end_time": str(sortie.end_time.strftime('%I:%M:%S %p')),
                    "duration": sortie.duration
                }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def update_sortie_by_id(data):
        try:
            sortie = Sortie.query.filter_by(id=data['id'],validity=1).first()
            if sortie:
                sortie.mission_planner_id = data.get('mission_planner_id',sortie.mission_planner_id )
                sortie.start_date = data.get('start_date',sortie.start_date)
                sortie.end_date = data.get('end_date',sortie.end_date)
                sortie.start_time = data.get('start_time',sortie.start_time)
                sortie.end_time = data.get('end_time',sortie.end_time)
                sortie.duration = data.get('duration',sortie.duration)
                db.session.commit()
                return {
                    "id": sortie.id,
                    "mission_planner_id": sortie.mission_planner_id,
                    "start_date": sortie.start_date.strftime('%d-%m-%Y'),
                    "start_time": str(sortie.start_time.strftime('%I:%M:%S %p')),
                    "end_date": sortie.end_date.strftime('%d-%m-%Y'),
                    "end_time": str(sortie.end_time.strftime('%I:%M:%S %p')),
                    "duration": sortie.duration
                }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def delete_sortie_by_id(id):
        try:
            sortie = Sortie.query.filter_by(id=id,validity=1).first()
            if sortie:
                sortie.validity = 0
                db.session.commit()

                return {
                    "id": sortie.id,
                    "mission_planner_id": sortie.mission_planner_id,
                    "start_date": sortie.start_date.strftime('%d-%m-%Y'),
                    "start_time": str(sortie.start_time.strftime('%I:%M:%S %p')),
                    "end_date": sortie.end_date.strftime('%d-%m-%Y'),
                    "end_time": str(sortie.end_time.strftime('%I:%M:%S %p')),
                    "duration": sortie.duration
                }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}