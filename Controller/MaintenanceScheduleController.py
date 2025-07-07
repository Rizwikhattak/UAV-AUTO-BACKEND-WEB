from config import db
from Model import MaintenanceSchedule, MissionPlanner


class MaintenanceScheduleController:

    # ──────────────── CREATE ────────────────
    @staticmethod
    def insert_maintenance_schedule(data):
        try:
            ms = MaintenanceSchedule(
                mission_planner_id=data["mission_planner_id"],
                dateFrom=data["dateFrom"],
                dateTo=data["dateTo"],
                label=data.get("label")
            )
            db.session.add(ms)
            db.session.commit()
            return {
                "id": ms.id,
                "mission_planner_id": ms.mission_planner_id,
                "dateFrom": str(ms.dateFrom),
                "dateTo": str(ms.dateTo),
                "label": ms.label
            }
        except Exception as e:
            print(e)
            return {}

    # ──────────────── UPDATE ────────────────
    @staticmethod
    def update_maintenance_schedule(data):
        try:
            ms = MaintenanceSchedule.query.filter_by(
                id=data.get("id"),
                validity=1
            ).first()

            if ms:
                ms.mission_planner_id = data.get("mission_planner_id", ms.mission_planner_id)
                ms.dateFrom         = data.get("dateFrom", ms.dateFrom)
                ms.dateTo           = data.get("dateTo", ms.dateTo)
                ms.label            = data.get("label", ms.label)

                db.session.commit()
                return {
                    "id": ms.id,
                    "mission_planner_id": ms.mission_planner_id,
                    "dateFrom": str(ms.dateFrom),
                    "dateTo": str(ms.dateTo),
                    "label": ms.label
                }
            return {}
        except Exception as e:
            print(e)
            return {}

    # ──────────────── DELETE (soft) ─────────
    @staticmethod
    def delete_maintenance_schedule_by_id(id):
        try:
            ms = MaintenanceSchedule.query.filter_by(id=id, validity=1).first()
            if ms:
                ms.validity = 0
                db.session.commit()
                return {
                    "id": ms.id,
                    "mission_planner_id": ms.mission_planner_id,
                    "dateFrom": str(ms.dateFrom),
                    "dateTo": str(ms.dateTo),
                    "label": ms.label
                }
            return {}
        except Exception as e:
            print(e)
            return {}

    # ──────────────── READ (all) ────────────
    @staticmethod
    def get_all_maintenance_schedule():
        try:
            all_ms = MaintenanceSchedule.query.filter_by(validity=1).all()
            return [
                {
                    "id": ms.id,
                    "mission_planner_id": ms.mission_planner_id,
                    "dateFrom": str(ms.dateFrom),
                    "dateTo": str(ms.dateTo),
                    "label": ms.label
                } for ms in all_ms
            ]
        except Exception as e:
            print(e)
            return []

    # ──────────────── READ m(one) ────────────
    @staticmethod
    def get_maintenance_schedule_by_id(id):
        try:
            ms = MaintenanceSchedule.query.filter_by(id=id, validity=1).first()
            if ms:
                return {
                    "id": ms.id,
                    "mission_planner_id": ms.mission_planner_id,
                    "dateFrom": str(ms.dateFrom),
                    "dateTo": str(ms.dateTo),
                    "label": ms.label
                }
            return {}
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def get_scheduled_missions():
        try:
            missions = MissionPlanner.query.filter_by(status='completed',validity=1).all()
            if missions:
                scheduled_missions = []
                for mission in missions:
                    sch_mission = MaintenanceSchedule.query.filter_by(mission_planner_id=mission['id'],validity=1).first()
                    dict = {**mission}
                    if sch_mission:
                        dict['scheduled'] = True
                    else:
                        dict['scheduled'] = False
                    scheduled_missions.append(dict)
                return scheduled_missions
            return {}
        except Exception as e:
            print(e)
            return {}
