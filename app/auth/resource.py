#### imports ####
from app import db
from flask import Response, request, jsonify
from flask_restful import Resource, Api
from models import Users, UsersSchema
from datetime import datetime

#### class defination ####
class UserByUsername(Resource):
    '''
    Get User by username
    Input: username
    Output: {user: data}
    '''
    def get(self,username):
        user = Users.query.filter_by(username=username).first()
        user_schema = UsersSchema()
        output = user_schema.dump(user)
        return jsonify({'user': output})
    def post(self):
        pass
    def put(self, id):
        pass
    def delete(self, id):
        pass


class UserByEmail(Resource):
    '''
    Get User by Email
    Input: email
    Output: {user: data}
    '''
    def get(self,email):
        user = Users.query.filter_by(email=email).first()
        user_schema = UsersSchema()
        output = user_schema.dump(user)
        return jsonify({'user': output})
    def post(self):
        pass
    def put(self, id):
        pass
    def delete(self, id):
        pass


class UserOperations(Resource):
    def get(self):
        pass
    '''
    POST user
    Input: username, email and password
    Output: user_id
    '''
    def post(self, username, email, password):
        user = Users(username=username.lower(), email=email, last_login=datetime.now())
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user.user_id
    def put(self, id):
        pass
    def delete(self, id):
        pass

    '''
    Check if valid user
    Input: username and password_hash
    Output: resultset or ''
    '''
    def is_user(self, username, password_hash):
        result = Users.query.filter_by(username=username).first()
        if result is not None:
            return result.check_password(password_hash)
        else:
            return result