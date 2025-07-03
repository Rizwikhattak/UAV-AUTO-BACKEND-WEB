from config import db, app
from Model import  SolarPanelEfficiency


class SolarPanelEfficiencyController:

    @staticmethod
    def insert_solar_panel_efficiency(data):
        try:
            response = []
            for eff in data:
                solar_panel_efficiency = SolarPanelEfficiency(label=eff['label'], efficiency_pct=eff['efficiency_pct'])
                db.session.add(solar_panel_efficiency)
                db.session.commit()
                response.append({
                    "id": solar_panel_efficiency.id,
                    "label": solar_panel_efficiency.label,
                    "efficiency_pct": solar_panel_efficiency.efficiency_pct,
                })
            return response
        except Exception as e:
            print(e)
            return {}


    @staticmethod
    def update_solar_panel_efficiency(data):
        try:
            response = []
            for eff in data:
                solar_panel_efficiency = SolarPanelEfficiency.query.filter_by(id=eff.get('id'), validity=1).first()
                if solar_panel_efficiency:
                    solar_panel_efficiency.label = eff.get('label', solar_panel_efficiency.label)
                    solar_panel_efficiency.efficiency_pct = eff.get('efficiency_pct', solar_panel_efficiency.efficiency_pct)
                    db.session.commit()
                    response.append({
                        "id": solar_panel_efficiency.id,
                        "label": solar_panel_efficiency.label,
                        "efficiency_pct": solar_panel_efficiency.efficiency_pct,
                    })
                else:
                    new_solar_panel_efficiency = SolarPanelEfficiency(label=eff['label'],
                                                                  efficiency_pct=eff['efficiency_pct'])
                    db.session.add(new_solar_panel_efficiency)
                    db.session.commit()
                    response.append({
                        "id": new_solar_panel_efficiency.id,
                        "label": new_solar_panel_efficiency.label,
                        "efficiency_pct": new_solar_panel_efficiency.efficiency_pct,
                    })
            return response
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def delete_solar_panel_efficiency_by_id(id):
        try:
            solar_panel_eff = SolarPanelEfficiency.query.filter_by(id=id, validity=1).first()
            if solar_panel_eff :
                solar_panel_eff.validity = 0
                db.session.commit()
                return {'id': solar_panel_eff.id,
                        'label': solar_panel_eff.label,
                        'efficiency_pct': solar_panel_eff.efficiency_pct,
                    }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def get_all_solar_panel_efficiency():
        try:
            solar_panel_efficiencies = (db.session.query(SolarPanelEfficiency)
                         .filter(SolarPanelEfficiency.validity == 1)
                         .all())
            if solar_panel_efficiencies:
                return [
                    {"id": eff.id,
                     "label": eff.label,
                     "efficiency_pct": eff.efficiency_pct,
                     } for eff in solar_panel_efficiencies]
            else:
                return []
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def get_solar_panel_efficiency_by_id(id):
        try:
            solar_panel_eff = (db.session.query(SolarPanelEfficiency)
                              .filter(SolarPanelEfficiency.id == id, SolarPanelEfficiency.validity == 1)
                              .first())
            if solar_panel_eff:
                return  {"id": solar_panel_eff.id,
                         "label": solar_panel_eff.label,
                         "efficiency_pct": solar_panel_eff.efficiency_pct,
                     }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}
