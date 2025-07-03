# Controller/MissionPanelMapController.py
from config import db
from Model import MissionPanelMap

class MissionPanelMapController:

    # ───────────────────────────── CREATE ──────────────────────────────
    @staticmethod
    def insert_mission_panel_map(data):
        try:
            mpm = MissionPanelMap(
                mission_planner_id=data['mission_planner_id'],
                solar_row         =data['solar_row'],
                solar_column      =data.get('solar_column'),
                solar_watts       =data.get('solar_watts'),
                solar_frame_no    =data.get('solar_frame_no')
            )
            db.session.add(mpm)
            db.session.commit()
            return {
                "id": mpm.id,
                "mission_planner_id": mpm.mission_planner_id,
                "solar_row": mpm.solar_row,
                "solar_column": mpm.solar_column,
                "solar_watts": mpm.solar_watts,
                "solar_frame_no": mpm.solar_frame_no
            }
        except Exception as e:
            print(e)
            return {}

    # ───────────────────────────── UPDATE ─────────────────────────────
    @staticmethod
    def update_mission_panel_map(data):
        try:
            mpm = MissionPanelMap.query.filter_by(
                id=data.get('id'),
                validity=1
            ).first()

            if mpm:
                mpm.mission_planner_id = data.get(
                    'mission_planner_id', mpm.mission_planner_id
                )
                mpm.solar_row      = data.get('solar_row',      mpm.solar_row)
                mpm.solar_column   = data.get('solar_column',   mpm.solar_column)
                mpm.solar_watts    = data.get('solar_watts',    mpm.solar_watts)
                mpm.solar_frame_no = data.get('solar_frame_no', mpm.solar_frame_no)

                db.session.commit()
                return {
                    "id": mpm.id,
                    "mission_planner_id": mpm.mission_planner_id,
                    "solar_row": mpm.solar_row,
                    "solar_column": mpm.solar_column,
                    "solar_watts": mpm.solar_watts,
                    "solar_frame_no": mpm.solar_frame_no
                }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

    # ───────────────────────────── DELETE ─────────────────────────────
    @staticmethod
    def delete_mission_panel_map_by_id(id):
        try:
            mpm = MissionPanelMap.query.filter_by(id=id, validity=1).first()
            if mpm:
                mpm.validity = 0   # soft-delete
                db.session.commit()
                return {
                    "id": mpm.id,
                    "mission_planner_id": mpm.mission_planner_id,
                    "solar_row": mpm.solar_row,
                    "solar_column": mpm.solar_column,
                    "solar_watts": mpm.solar_watts,
                    "solar_frame_no": mpm.solar_frame_no
                }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

    # ───────────────────────────── READ (ALL) ─────────────────────────
    @staticmethod
    def get_all_mission_panel_map():
        try:
            mpms = MissionPanelMap.query.filter_by(validity=1).all()
            return [
                {
                    "id": mpm.id,
                    "mission_planner_id": mpm.mission_planner_id,
                    "solar_row": mpm.solar_row,
                    "solar_column": mpm.solar_column,
                    "solar_watts": mpm.solar_watts,
                    "solar_frame_no": mpm.solar_frame_no
                }
                for mpm in mpms
            ]
        except Exception as e:
            print(e)
            return []

    # ───────────────────────────── READ (ONE) ─────────────────────────
    @staticmethod
    def get_mission_panel_map_by_id(id):
        try:
            mpm = MissionPanelMap.query.filter_by(id=id, validity=1).first()
            if mpm:
                return {
                    "id": mpm.id,
                    "mission_planner_id": mpm.mission_planner_id,
                    "solar_row": mpm.solar_row,
                    "solar_column": mpm.solar_column,
                    "solar_watts": mpm.solar_watts,
                    "solar_frame_no": mpm.solar_frame_no
                }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}
