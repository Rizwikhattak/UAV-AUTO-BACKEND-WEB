from flask import Blueprint, jsonify, request
from Controller import MaintenancePersonalController
from config import app   # kept for stylistic consistency

maintenance_personal_routes = Blueprint(
    "maintenance_personal_routes", __name__
)

# ─────────────── CREATE ───────────────
@maintenance_personal_routes.route(
    "/insert_maintenance_personal",
    methods=["POST"]
)
def insert_maintenance_personal():
    data = request.get_json()
    result = MaintenancePersonalController.insert_maintenance_personal(data)
    if result:
        return jsonify({"success": True, "data": result}), 200
    return jsonify({"success": False, "data": result}), 400


# ─────────────── UPDATE ───────────────
@maintenance_personal_routes.route(
    "/update_maintenance_personal_by_id/<int:id>",
    methods=["PUT"]
)
def update_maintenance_personal_by_id(id):
    data = request.get_json()
    data["id"] = id
    result = MaintenancePersonalController.update_maintenance_personal(data)
    if result:
        return jsonify({"success": True, "data": result}), 200
    return jsonify({"success": False, "data": result}), 400


# ─────────────── DELETE ───────────────
@maintenance_personal_routes.route(
    "/delete_maintenance_personal_by_id/<int:id>",
    methods=["DELETE"]
)
def delete_maintenance_personal_by_id(id):
    result = MaintenancePersonalController.delete_maintenance_personal_by_id(id)
    if result:
        return jsonify({"success": True, "data": result}), 200
    return jsonify({"success": False, "data": result}), 400


# ─────────────── READ (all) ────────────
@maintenance_personal_routes.route(
    "/get_all_maintenance_personal",
    methods=["GET"]
)
def get_all_maintenance_personal():
    result = MaintenancePersonalController.get_all_maintenance_personal()
    if result:
        return jsonify({"success": True, "data": result}), 200
    return jsonify({"success": False, "data": result}), 400


# ─────────────── READ (one) ────────────
@maintenance_personal_routes.route(
    "/get_maintenance_personal_by_id/<int:id>",
    methods=["GET"]
)
def get_maintenance_personal_by_id(id):
    result = MaintenancePersonalController.get_maintenance_personal_by_id(id)
    if result:
        return jsonify({"success": True, "data": result}), 200
    return jsonify({"success": False, "data": result}), 400
