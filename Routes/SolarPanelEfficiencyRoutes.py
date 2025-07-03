# routes/solar_panel_efficiency_routes.py

from flask import Blueprint, jsonify, request
from Controller import SolarPanelEfficiencyController
from config import app  # keep style consistent even if not used directly

# Create a blueprint for solar-panel-efficiency routes
solar_panel_efficiency_routes = Blueprint(
    'solar_panel_efficiency_routes', __name__
)


# ───────────────────────────── CREATE ──────────────────────────────
@solar_panel_efficiency_routes.route(
    '/insert_solar_panel_efficiency',
    methods=['POST']
)
def insert_solar_panel_efficiency():
    data = request.get_json()
    result = SolarPanelEfficiencyController.insert_solar_panel_efficiency(data)
    if result:
        return jsonify({'success': True, 'data': result}), 200
    else:
        return jsonify({'success': False, 'data': result}), 400


# ───────────────────────────── UPDATE ──────────────────────────────
@solar_panel_efficiency_routes.route(
    '/update_solar_panel_efficiency_by_id',
    methods=['PUT']
)
def update_solar_panel_efficiency_by_id():
    data = request.get_json()
    result = SolarPanelEfficiencyController.update_solar_panel_efficiency(data)
    if result:
        return jsonify({'success': True, 'data': result}), 200
    else:
        return jsonify({'success': False, 'data': result}), 400


# ───────────────────────────── DELETE ──────────────────────────────
@solar_panel_efficiency_routes.route(
    '/delete_solar_panel_efficiency_by_id/<int:id>',
    methods=['DELETE']
)
def delete_solar_panel_efficiency_by_id(id):
    result = SolarPanelEfficiencyController.delete_solar_panel_efficiency_by_id(id)
    if result:
        return jsonify({'success': True, 'data': result}), 200
    else:
        return jsonify({'success': False, 'data': result}), 400


# ───────────────────────────── READ (ALL) ──────────────────────────
@solar_panel_efficiency_routes.route(
    '/get_all_solar_panel_efficiency',
    methods=['GET']
)
def get_all_solar_panel_efficiency():
    result = SolarPanelEfficiencyController.get_all_solar_panel_efficiency()
    if result:
        return jsonify({'success': True, 'data': result}), 200
    else:
        return jsonify({'success': False, 'data': result}), 400


# ───────────────────────────── READ (ONE) ──────────────────────────
@solar_panel_efficiency_routes.route(
    '/get_solar_panel_efficiency_by_id/<int:id>',
    methods=['GET']
)
def get_solar_panel_efficiency_by_id(id):
    result = SolarPanelEfficiencyController.get_solar_panel_efficiency_by_id(id)
    if result:
        return jsonify({'success': True, 'data': result}), 200
    else:
        return jsonify({'success': False, 'data': result}), 400
