from config import db
from Model import MaintenancePersonal
from werkzeug.security import generate_password_hash


class MaintenancePersonalController:

    # ─────────────── CREATE ───────────────
    @staticmethod
    def insert_maintenance_personal(data):
        try:
            mp = MaintenancePersonal(
                name=data["name"],
                email=data["email"],
                password=generate_password_hash(data["password"]),
                age=data.get("age"),
                gender=data.get("gender")
            )
            db.session.add(mp)
            db.session.commit()
            return {
                "id": mp.id,
                "name": mp.name,
                "email": mp.email,
                "age": mp.age,
                "gender": mp.gender
            }
        except Exception as e:
            print(e)
            return {}

    # ─────────────── UPDATE ───────────────
    @staticmethod
    def update_maintenance_personal(data):
        try:
            mp = MaintenancePersonal.query.filter_by(
                id=data.get("id"), validity=1
            ).first()

            if mp:
                mp.name   = data.get("name", mp.name)
                mp.email  = data.get("email", mp.email)
                mp.age    = data.get("age", mp.age)
                mp.gender = data.get("gender", mp.gender)

                if "password" in data and data["password"]:
                    mp.password = generate_password_hash(data["password"])

                db.session.commit()
                return {
                    "id": mp.id,
                    "name": mp.name,
                    "email": mp.email,
                    "age": mp.age,
                    "gender": mp.gender
                }
            return {}
        except Exception as e:
            print(e)
            return {}

    # ─────────────── DELETE (soft) ────────
    @staticmethod
    def delete_maintenance_personal_by_id(id):
        try:
            mp = MaintenancePersonal.query.filter_by(id=id, validity=1).first()
            if mp:
                mp.validity = 0
                db.session.commit()
                return {
                    "id": mp.id,
                    "name": mp.name,
                    "email": mp.email,
                    "age": mp.age,
                    "gender": mp.gender
                }
            return {}
        except Exception as e:
            print(e)
            return {}

    # ─────────────── READ (all) ───────────
    @staticmethod
    def get_all_maintenance_personal():
        try:
            all_mp = MaintenancePersonal.query.filter_by(validity=1).all()
            return [
                {
                    "id": mp.id,
                    "name": mp.name,
                    "email": mp.email,
                    "age": mp.age,
                    "gender": mp.gender
                } for mp in all_mp
            ]
        except Exception as e:
            print(e)
            return []

    # ─────────────── READ (one) ───────────
    @staticmethod
    def get_maintenance_personal_by_id(id):
        try:
            mp = MaintenancePersonal.query.filter_by(id=id, validity=1).first()
            if mp:
                return {
                    "id": mp.id,
                    "name": mp.name,
                    "email": mp.email,
                    "age": mp.age,
                    "gender": mp.gender
                }
            return {}
        except Exception as e:
            print(e)
            return {}
