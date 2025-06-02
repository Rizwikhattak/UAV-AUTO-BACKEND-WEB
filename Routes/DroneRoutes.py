from flask import Blueprint,jsonify,request,send_from_directory
from Controller import DroneController
from config import app

drone_routes = Blueprint('drone_routes',__name__)

@drone_routes.route('/insert_drone',methods=['POST'])
def insert_drone():
    data = request.form.to_dict()
    drone_img = request.files.get('image')
    drone = DroneController.insert_drone(data,drone_img)
    if drone:
        return jsonify({'success':True,'data':drone}),200
    else:
        return jsonify({'success':False,'data':drone}),400

@drone_routes.route('/update_drone_by_id/<int:id>', methods=['PUT'])
def update_drone_by_id(id):
    data = request.form.to_dict()
    data['id'] = id
    drone_img = request.files.get('image')
    drone = DroneController.update_drone_by_id(data, drone_img)
    if drone:
        return jsonify({'success':True,'data':drone}),200
    else:
        return jsonify({'success':False,'data':drone}),400

@drone_routes.route('/get_all_drones',methods=['GET'])
def get_all_drones():
    drones = DroneController.get_all_drones()
    if drones:
        return jsonify({'success':True,'data':drones}),200
    else:
        return jsonify({'success':False,'data':drones}),400

@drone_routes.route('/get_drone_by_id/<int:id>',methods=['GET'])
def get_drone_by_id(id):
    drone = DroneController.get_drone_by_id(id)
    if drone:
        return jsonify({'success':True,'data':drone}),200
    else:
        return jsonify({'success': False, 'data': drone}),400

@drone_routes.route('/delete_drone_by_id/<int:id>',methods=['DELETE'])
def delete_drone_by_id(id):
    drone = DroneController.delete_drone_by_id(id)

    if drone:
        return jsonify({'success':True,'data':drone}),200
    else:
        return jsonify({'success': False, 'data': drone}),400

@drone_routes.route('/uploads/drones/profile_pictures/<filename>')
def serve_profile_picture(filename):
    return send_from_directory(app.config['DRONE_PROFILE_PICTURES_FOLDER'], filename)

