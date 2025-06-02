from flask import Blueprint,request,jsonify
from Controller import DroneStationMappingController

drone_station_mapping_routes = Blueprint('drone_station_mapping_routes',__name__)

@drone_station_mapping_routes.route('/insert_drone_station_mapping',methods=['POST'])
def insert_drone_station_mapping():
    data = request.get_json()
    drone_station_mapping = DroneStationMappingController.insert_drone_sation_mapping(data)
    if drone_station_mapping:
        return jsonify({'success':True,'data':drone_station_mapping}),200
    else:
        return jsonify({'success':False,'data':drone_station_mapping}),400

@drone_station_mapping_routes.route('/get_all_drone_station_mappings',methods=['GET'])
def get_all_drone_station_mappings():
    drone_station_mappings = DroneStationMappingController.get_all_drone_station_mappings()
    if drone_station_mappings:
        return jsonify({'success':True,'data':drone_station_mappings}),200
    else:
        return jsonify({'success':False,'data':drone_station_mappings}),400

@drone_station_mapping_routes.route('/get_drone_station_mapping_by_id/<int:id>',methods=['GET'])
def get_drone_station_mapping_by_id(id):
    drone_station_mapping = DroneStationMappingController.get_drone_station_mapping_by_id(id)
    if drone_station_mapping:
        return jsonify({'success':True,'data':drone_station_mapping}),200
    else:
        return jsonify({'success':False,'data':drone_station_mapping}),400

@drone_station_mapping_routes.route('/update_drone_station_mapping_by_id/<int:id>',methods=['PUT'])
def update_drone_station_mapping(id):
    data = request.get_json()
    data['id'] = id
    drone_station_mapping = DroneStationMappingController.update_drone_station_mapping(data)
    if drone_station_mapping:
        return jsonify({'success':True,'data':drone_station_mapping}),200
    else:
        return jsonify({'success':False,'data':drone_station_mapping}),400

@drone_station_mapping_routes.route('/delete_drone_station_mapping_by_id/<int:id>',methods=['DELETE'])
def delete_drone_station_mapping_by_id(id):
    drone_station_mapping = DroneStationMappingController.delete_drone_station_mapping_by_id(id)
    if drone_station_mapping:
        return jsonify({'success':True,'data':drone_station_mapping}),200
    else:
        return jsonify({'success':False,'data':drone_station_mapping}),400

