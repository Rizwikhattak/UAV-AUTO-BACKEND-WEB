# routes/efficiency_report_routes.py
from flask import Blueprint, jsonify, request
from Controller import EfficiencyReportController
from config import app   # kept for stylistic consistency

efficiency_report_routes = Blueprint(
    'efficiency_report_routes', __name__
)

# ──────────────── CREATE ────────────────
@efficiency_report_routes.route(
    '/insert_efficiency_report',
    methods=['POST']
)
def insert_efficiency_report():
    data = request.get_json()
    result = EfficiencyReportController.insert_efficiency_report(data)
    if result:
        return jsonify({'success': True, 'data': result}), 200
    return jsonify({'success': False, 'data': result}), 400

# ──────────────── UPDATE ────────────────
@efficiency_report_routes.route(
    '/update_efficiency_report_by_id/<int:id>',
    methods=['PUT']
)
def update_efficiency_report_by_id(id):
    data = request.get_json()
    data['id'] = id
    result = EfficiencyReportController.update_efficiency_report(data)
    if result:
        return jsonify({'success': True, 'data': result}), 200
    return jsonify({'success': False, 'data': result}), 400

# ──────────────── DELETE ────────────────
@efficiency_report_routes.route(
    '/delete_efficiency_report_by_id/<int:id>',
    methods=['DELETE']
)
def delete_efficiency_report_by_id(id):
    result = EfficiencyReportController.delete_efficiency_report_by_id(id)
    if result:
        return jsonify({'success': True, 'data': result}), 200
    return jsonify({'success': False, 'data': result}), 400

# ──────────────── READ (all) ─────────────
@efficiency_report_routes.route(
    '/get_all_efficiency_report',
    methods=['GET']
)
def get_all_efficiency_report():
    result = EfficiencyReportController.get_all_efficiency_report()
    if result:
        return jsonify({'success': True, 'data': result}), 200
    return jsonify({'success': False, 'data': result}), 400

# ──────────────── READ (one) ─────────────
@efficiency_report_routes.route(
    '/get_efficiency_report_by_id/<int:id>',
    methods=['GET']
)
def get_efficiency_report_by_id(id):
    result = EfficiencyReportController.get_efficiency_report_by_id(id)
    if result:
        return jsonify({'success': True, 'data': result}), 200
    return jsonify({'success': False, 'data': result}), 400

@efficiency_report_routes.route(
    '/get_efficiency_reports_by_mission_id/<int:id>',
    methods=['GET']
)
def get_efficiency_reports_by_mission_id(id):
    result = EfficiencyReportController.get_efficiency_reports_by_mission_id(id)
    if result:
        return jsonify({'success': True, 'data': result}), 200
    return jsonify({'success': False, 'data': result}), 400
