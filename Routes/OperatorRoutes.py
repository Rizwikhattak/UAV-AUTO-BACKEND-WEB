from flask import Blueprint, jsonify, request,send_from_directory
from Controller import OperatorController
from config import app

# Create a blueprint for user routes
user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/login_user',methods=['POST'])
def login_user():
    data = request.get_json()
    user = OperatorController.login_operator(data)
    if user:
        return jsonify({'success':True,'data':user}),200
    else:
        return jsonify({'success':False,'data':user}),400

@user_routes.route('/insert_operator',methods=['POST'])
def insert_operator():
    data = request.get_json()
    operator = OperatorController.insert_operator(data)
    if operator:
        return jsonify({'success':True,'data':operator}),200
    else:
        return jsonify({'success':False,'data':operator}),400




@user_routes.route('/update_operator_by_id/<int:id>',methods=['PUT'])
def update_operator(id):
    data = request.get_json()
    data['id'] = id
    operator = OperatorController.update_operator(data,)
    if operator:
        return jsonify({'success':True,'data':operator}),200
    else:
        return jsonify({'success':False,'data':operator}),400

@user_routes.route('/delete_operator_by_id/<int:id>',methods=['DELETE'])
def delete_operator_by_id(id):
    operator = OperatorController.delete_operator_by_id(id)
    if operator:
        return jsonify({'success':True,'operator':operator}),200
    else:
        return jsonify({'success':False,'operator':operator}),400


@user_routes.route('/get_all_operators',methods=['GET'])
def get_all_operators():
    operators = OperatorController.get_all_operators()
    if operators:
        return jsonify({'success':True,'data':operators}),200
    else:
        return jsonify({'success':False,'data':operators}),400

@user_routes.route('/get_operator_by_id/<int:id>',methods=['GET'])
def get_operator_by_id(id):
    operator = OperatorController.get_operator_by_id(id)
    if operator:
        return jsonify({'success':True,'data':operator}),200
    else:
        return jsonify({'success':False,'data':operator}),400

