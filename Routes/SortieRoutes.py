from flask import Blueprint,request,jsonify
from Controller import SortieController

sortie_routes = Blueprint('sortie_routes',__name__)

@sortie_routes.route('/insert_sortie',methods=['POST'])
def insert_sortie():
    data = request.get_json()
    sortie = SortieController.insert_sortie(data)
    if sortie:
        return jsonify({'success':True,'data':sortie}),200
    else:
        return jsonify({'success':False,'data':{}}),400

@sortie_routes.route('/get_all_sorties',methods=['GET'])
def get_all_sorties():
    sorties = SortieController.get_all_sorties()
    if sorties:
        return jsonify({'success':True,'data':sorties}),200
    else:
        return jsonify({'success':False,'data':sorties}),400

@sortie_routes.route('/get_sortie_by_id/<int:id>',methods=['GET'])
def get_sortie_by_id(id):
    sortie = SortieController.get_sortie_by_id(id)
    if sortie:
        return jsonify({'success':True,'data':sortie}),200
    else:
        return jsonify({'success':False,'data':sortie},400)

@sortie_routes.route('/update_sortie_by_id/<int:id>',methods=['PUT'])
def update_sortie_by_id(id):
    data = request.get_json()
    data['id'] = id
    sortie = SortieController.update_sortie_by_id(data)
    if sortie:
        return jsonify({'success':True,'data':sortie}),200
    else:
        return jsonify({'success':False,'data':{}}),400

@sortie_routes.route('/delete_sortie_by_id/<int:id>',methods=['DELETE'])
def delete_sortie_by_id(id):
    sortie = SortieController.delete_sortie_by_id(id)
    if sortie:
        return jsonify({'success':True,'data':sortie}),200
    else:
        return jsonify({'success':False,'data':{}}),400