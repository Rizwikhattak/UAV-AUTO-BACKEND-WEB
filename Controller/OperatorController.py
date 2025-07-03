from config import db, app
from Model import  Operator
from werkzeug.security import generate_password_hash, check_password_hash



class OperatorController:

    @staticmethod
    def insert_operator(data):
        try:
            hashed_password = generate_password_hash(data['password'])
            op = Operator(name=data['name'], password=hashed_password, age=data['age'], email=data['email'],gender=data['gender'])
            db.session.add(op)
            db.session.commit()
            return {
                "id": op.id,
                "name": op.name,
                "gender":op.gender,
                "age": op.age,
                "email": op.email
            }
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def login_operator(data):
        try:
            email = data['email']
            password = data['password']
            user = Operator.query.filter_by(email=email, validity=1).first()
            if user is not None:
                print("user password", user.password)
                print("password", password)
                print("is valid", check_password_hash(user.password, password))
                if check_password_hash(user.password, password):
                    return {'name': user.name, 'email': user.email, 'id': user.id}
                else:
                    return {}
            else:
                return {}
        except Exception as e:
            print(e)
            return {}



    @staticmethod
    def update_operator(data):
        try:
            op = Operator.query.filter_by(id=data.get('id'), validity=1).first()
            if op:
                Operator.name = data.get('name', op.name)
                Operator.email = data.get('email', op.email)
                Operator.password = generate_password_hash(data.get('password', op.password))
                Operator.age = data.get('age', op.age)
                Operator.gender = data.get('gender', op.gender)
                db.session.commit()
                return {
                    "id": op.id,
                    "name": op.name,
                    "email": op.email,
                    "age": op.age,
                    "gender": op.gender,

                }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def delete_operator_by_id(operator_id):
        try:
            operator = Operator.query.filter_by(id=operator_id, validity=1).first()
            if operator :
                operator.validity = 0
                db.session.commit()
                return {'id': operator.id, 'name': operator.name, 'email': operator.email,
                        }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def get_all_operators():
        try:
            operators = (db.session.query(Operator)
                         .filter(Operator.validity == 1)
                         .all())
            if operators:
                return [
                    {"id": operator.id, "name": operator.name, "age": operator.age, "email": operator.email, "gender":operator.gender,
                     } for operator in operators]
            else:
                return []
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def get_operator_by_id(operator_id):
        try:
            operator = (db.session.query(Operator)
                              .filter(Operator.id == operator_id, Operator.validity == 1)
                              .first())
            if operator:
                return  {"id": operator.id, "name": operator.name, "age": operator.age, "email": operator.email, "gender":operator.gender,
                     }
            else:
                return {}
        except Exception as e:
            print(e)
            return {}
