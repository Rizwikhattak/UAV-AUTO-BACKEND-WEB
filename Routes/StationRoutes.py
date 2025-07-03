from flask import Blueprint,request,jsonify
from Controller import StationController

station_routes = Blueprint('station_routes',__name__)

@station_routes.route('/insert_station',methods=['POST'])
def insert_station():
    data = request.get_json()
    station = StationController.insert_station(data)
    if station:
        return jsonify({'success':True,'data':station}),200
    else:
        return jsonify({'success':False,'data':station}),400

@station_routes.route('/get_all_stations',methods=['GET'])
def get_all_stations():
    stations = StationController.get_all_stations()
    if stations:
        return jsonify({'success':True,'data':stations}),200
    else:
        return jsonify({'success':False,'data':stations}),400

@station_routes.route('/get_station_by_id/<int:id>',methods=['GET'])
def get_station_by_id(id):
    station = StationController.get_station_by_id(id)
    if station:
        return jsonify({'success':True,'data':station}),200
    else:
        return jsonify({'success':False,'data':station}),400

@station_routes.route('/update_station_by_id/<int:id>',methods=['PUT'])
def update_station_by_id(id):
    data = request.get_json()
    data['id'] = id
    station = StationController.update_station_by_id(data)
    if station:
        return jsonify({'success':True,'data':station}),200
    else:
        return jsonify({'success':False,'data':station}),400

@station_routes.route('/delete_station_by_id/<int:id>',methods=['DELETE'])
def delete_station(id):
    station = StationController.delete_station_by_id(id)
    if station:
        return jsonify({'success':True,'data':station}),200
    else:
        return jsonify({'success':False,'data':station}),400
