# Controller/EfficiencyReportController.py
from Controller import MissionPanelMapController, SolarPanelEfficiencyController
from config import db
from Model import EfficiencyReport

class EfficiencyReportController:

    # ──────────────── CREATE ────────────────
    @staticmethod
    def insert_efficiency_report(data):
        try:
            efficiencies = SolarPanelEfficiencyController.get_all_solar_panel_efficiency()
            res = 0
            if efficiencies:
                for eff in efficiencies:
                    if eff["label"] == data['label']:
                        eff_pct = eff["efficiency_pct"]
                        solar_wats =data["solar_watts"]
                        res = (eff_pct/100) * solar_wats

                er = EfficiencyReport(
                    mission_planner_id = data['mission_planner_id'],
                    mission_panel_map_id = data['mission_panel_map_id'],
                    label = data['label'],
                    calculated_efficiency = res
                )
                db.session.add(er)
                db.session.commit()
                return {
                    "id": er.id,
                    "mission_planner_id": er.mission_planner_id,
                    "mission_panel_map_id": er.mission_panel_map_id,
                    "label": er.label,
                    "calculated_efficiency": er.calculated_efficiency
                }
            return {}
        except Exception as e:
            print(e)
            return {}

    # ──────────────── UPDATE ────────────────
    @staticmethod
    def update_efficiency_report(data):
        try:
            er = EfficiencyReport.query.filter_by(
                id=data.get('id'),
                validity=1
            ).first()
            if er:
                er.mission_planner_id   = data.get('mission_planner_id', er.mission_planner_id)
                er.mission_panel_map_id = data.get('mission_panel_map_id', er.mission_panel_map_id)
                er.label                = data.get('label', er.label)
                er.calculated_efficiency= data.get('calculated_efficiency', er.calculated_efficiency)
                db.session.commit()
                return {
                    "id": er.id,
                    "mission_planner_id": er.mission_planner_id,
                    "mission_panel_map_id": er.mission_panel_map_id,
                    "label": er.label,
                    "calculated_efficiency": er.calculated_efficiency
                }
            return {}
        except Exception as e:
            print(e)
            return {}

    # ──────────────── DELETE (soft) ─────────
    @staticmethod
    def delete_efficiency_report_by_id(id):
        try:
            er = EfficiencyReport.query.filter_by(id=id, validity=1).first()
            if er:
                er.validity = 0
                db.session.commit()
                return {
                    "id": er.id,
                    "mission_planner_id": er.mission_planner_id,
                    "mission_panel_map_id": er.mission_panel_map_id,
                    "label": er.label,
                    "calculated_efficiency": er.calculated_efficiency
                }
            return {}
        except Exception as e:
            print(e)
            return {}

    # ──────────────── READ (all) ────────────
    @staticmethod
    def get_all_efficiency_report():
        try:
            ers = EfficiencyReport.query.filter_by(validity=1).all()
            return [
                {
                    "id": er.id,
                    "mission_planner_id": er.mission_planner_id,
                    "mission_panel_map_id": er.mission_panel_map_id,
                    "label": er.label,
                    "calculated_efficiency": er.calculated_efficiency
                } for er in ers
            ]
        except Exception as e:
            print(e)
            return []

    # ──────────────── READ (one) ────────────
    @staticmethod
    def get_efficiency_report_by_id(id):
        try:
            er = EfficiencyReport.query.filter_by(id=id, validity=1).first()
            if er:
                return {
                    "id": er.id,
                    "mission_planner_id": er.mission_planner_id,
                    "mission_panel_map_id": er.mission_panel_map_id,
                    "label": er.label,
                    "calculated_efficiency": er.calculated_efficiency
                }
            return {}
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def get_efficiency_reports_by_mission_id(id):
        try:
            ers = EfficiencyReport.query.filter_by(mission_planner_id=id, validity=1).all()
            if ers:
                return [{
                    "id": er.id,
                    "mission_planner_id": er.mission_planner_id,
                    "mission_panel_map_id": er.mission_panel_map_id,
                    "label": er.label,
                    "calculated_efficiency": er.calculated_efficiency
                } for er in ers]
            return {}
        except Exception as e:
            print(e)
            return {}
