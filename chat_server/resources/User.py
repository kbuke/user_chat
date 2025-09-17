from config import db

from flask import request, make_response, session
from flask_restful import Resource

from models.User import UserModel

class UserList(Resource):
    def get(self):
        users = [user.to_dict() for user in UserModel.query.all()]
        return users
    
    def post(self):
        json = request.get_json()

        try:
            new_user = UserModel(
                username = json.get("username"),
                gender = json.get("gender"),
                profile_picture = json.get("profilePic"),
                allow_all_messages = json.get("messageRestrictions"),
            )
            new_user.password_hash = json.get("newPassword")
            db.session.add(new_user)
            db.session.commit()
            return {"message": "New User Registered"}, 201
        except ValueError as e:
            return {"error": [str(e)]}, 400

class User(Resource):
    def get(self, id):
        user = UserModel.query.filter(UserModel.id == id).first()
        if user:
            return user.to_dict(), 201
        else:
            return{"error": f"User {id} not registered."}, 404
        
    def delete(self, id):
        user = UserModel.query.filter(UserModel.id == id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": f"User {id} deleted"}, 201
        else:
            return {"error": f"User {id} not found"}, 404