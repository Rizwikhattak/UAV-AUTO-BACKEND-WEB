# routes/mission_panel_map_routes.py
from flask import Blueprint, jsonify, request
from Controller import MissionPanelMapController
from config import app   # kept for consistency

mission_panel_map_routes = Blueprint(
    'mission_panel_map_routes', __name__
)

# ─────────────────────────── CREATE ────────────────────────────
@mission_panel_map_routes.route(
    '/insert_mission_panel_map',
    methods=['POST']
)
def insert_mission_panel_map():
    data = request.get_json()
    result = MissionPanelMapController.insert_mission_panel_map(data)
    if result:
        return jsonify({'success': True, 'data': result}), 200
    else:
        return jsonify({'success': False, 'data': result}), 400

# ─────────────────────────── UPDATE ────────────────────────────
@mission_panel_map_routes.route(
    '/update_mission_panel_map_by_id/<int:id>',
    methods=['PUT']
)
def update_mission_panel_map_by_id(id):
    data = request.get_json()
    data['id'] = id
    result = MissionPanelMapController.update_mission_panel_map(data)
    if result:
        return jsonify({'success': True, 'data': result}), 200
    else:
        return jsonify({'success': False, 'data': result}), 400

# ─────────────────────────── DELETE ────────────────────────────
@mission_panel_map_routes.route(
    '/delete_mission_panel_map_by_id/<int:id>',
    methods=['DELETE']
)
def delete_mission_panel_map_by_id(id):
    result = MissionPanelMapController.delete_mission_panel_map_by_id(id)
    if result:
        return jsonify({'success': True, 'data': result}), 200
    else:
        return jsonify({'success': False, 'data': result}), 400

# ─────────────────────────── READ (ALL) ────────────────────────
@mission_panel_map_routes.route(
    '/get_all_mission_panel_map',
    methods=['GET']
)
def get_all_mission_panel_map():
    result = MissionPanelMapController.get_all_mission_panel_map()
    if result:
        return jsonify({'success': True, 'data': result}), 200
    else:
        return jsonify({'success': False, 'data': result}), 400

# ─────────────────────────── READ (ONE) ────────────────────────
@mission_panel_map_routes.route(
    '/get_mission_panel_map_by_id/<int:id>',
    methods=['GET']
)
def get_mission_panel_map_by_id(id):
    result = MissionPanelMapController.get_mission_panel_map_by_id(id)
    if result:
        return jsonify({'success': True, 'data': result}), 200
    else:
        return jsonify({'success': False, 'data': result}), 400

@mission_panel_map_routes.route(
    '/get_mission_panel_maps_by_mission_id/<int:id>',
    methods=['GET']
)
def get_mission_panel_maps_by_mission_id(id):
    result = MissionPanelMapController.get_mission_panel_maps_by_mission_id(id)
    if result:
        return jsonify({'success': True, 'data': result}), 200
    else:
        return jsonify({'success': False, 'data': result}), 400
