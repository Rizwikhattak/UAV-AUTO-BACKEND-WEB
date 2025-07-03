from flask import Blueprint, jsonify, request
from Controller import MaintenanceScheduleController
from config import app   # kept for consistency

maintenance_schedule_routes = Blueprint(
    "maintenance_schedule_routes", __name__
)

# ──────────────── CREATE ────────────────
@maintenance_schedule_routes.route(
    "/insert_maintenance_schedule",
    methods=["POST"]
)
def insert_maintenance_schedule():
    data = request.get_json()
    result = MaintenanceScheduleController.insert_maintenance_schedule(data)
    if result:
        return jsonify({"success": True, "data": result}), 200
    return jsonify({"success": False, "data": result}), 400


# ──────────────── UPDATE ────────────────
@maintenance_schedule_routes.route(
    "/update_maintenance_schedule_by_id/<int:id>",
    methods=["PUT"]
)
def update_maintenance_schedule_by_id(id):
    data = request.get_json()
    data["id"] = id
    result = MaintenanceScheduleController.update_maintenance_schedule(data)
    if result:
        return jsonify({"success": True, "data": result}), 200
    return jsonify({"success": False, "data": result}), 400


# ──────────────── DELETE ────────────────
@maintenance_schedule_routes.route(
    "/delete_maintenance_schedule_by_id/<int:id>",
    methods=["DELETE"]
)
def delete_maintenance_schedule_by_id(id):
    result = MaintenanceScheduleController.delete_maintenance_schedule_by_id(id)
    if result:
        return jsonify({"success": True, "data": result}), 200
    return jsonify({"success": False, "data": result}), 400


# ──────────────── READ (all) ─────────────
@maintenance_schedule_routes.route(
    "/get_all_maintenance_schedule",
    methods=["GET"]
)
def get_all_maintenance_schedule():
    result = MaintenanceScheduleController.get_all_maintenance_schedule()
    if result:
        return jsonify({"success": True, "data": result}), 200
    return jsonify({"success": False, "data": result}), 400


# ──────────────── READ (one) ─────────────
@maintenance_schedule_routes.route(
    "/get_maintenance_schedule_by_id/<int:id>",
    methods=["GET"]
)
def get_maintenance_schedule_by_id(id):
    result = MaintenanceScheduleController.get_maintenance_schedule_by_id(id)
    if result:
        return jsonify({"success": True, "data": result}), 200
    return jsonify({"success": False, "data": result}), 400
