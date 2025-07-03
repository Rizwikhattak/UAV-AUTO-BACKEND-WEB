from flask import Blueprint,request,jsonify
from Controller import DroneAvailabilityLogController

drone_availability_log_routes = Blueprint('drone_availability_log_routes',__name__)

@drone_availability_log_routes.route('/insert_drone_availability_log',methods=['POST'])
def insert_drone_availability_log():
    data = request.get_json()
    drone_availability_log = DroneAvailabilityLogController.insert_drone_availability_log(data)
    if drone_availability_log:
        return jsonify({'success':True,'data':drone_availability_log}),200
    else:
        return jsonify({'success':False,'data':drone_availability_log}),400

@drone_availability_log_routes.route('/get_all_drone_availability_logs',methods=['GET'])
def get_all_drone_availability_logs():
    data = DroneAvailabilityLogController.get_all_drone_availability_logs()
    if data:
        return jsonify({'success':True,'data':data}),200
    else:
        return jsonify({'success':False,'data':data}),400

@drone_availability_log_routes.route('/get_drone_availability_log_by_id/<int:id>',methods=['GET'])
def get_drone_availability_log_by_id(id):
    data = DroneAvailabilityLogController.get_drone_availability_log_by_id(id)
    if data:
        return jsonify({'success':True,'data':data}),200
    else:
        return jsonify({'success':False,'data':data}),400

@drone_availability_log_routes.route('/update_drone_availability_log_by_id/<int:id>',methods=['PUT'])
def update_drone_availability_log_by_id(id):
    data = request.get_json()
    data['id'] = id
    drone_availability_log = DroneAvailabilityLogController.update_drone_availability_log_by_id(data)
    if drone_availability_log:
        return jsonify({'success':True,'data':drone_availability_log}),200
    else:
        return jsonify({'success':False,'data':drone_availability_log}),400

@drone_availability_log_routes.route('/delete_drone_availability_log_by_id/<int:id>',methods=['DELETE'])
def delete_drone_availability_log_by_id(id):
    data = DroneAvailabilityLogController.delete_drone_availability_log_by_id(id)
    if data:
        return jsonify({'success':True,'data':data}),200
    else:
        return jsonify({'success':False,'data':data}),400