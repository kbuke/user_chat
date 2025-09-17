from models.Followers import FollowerModel

from config import db

from flask_restful import Resource
from flask import request

class FollowersList(Resource):
    def get(self):
        followers = [follower.to_dict() for follower in FollowerModel.query.all()]
        return followers
    
    def post(self):
        json = request.get_json()
        try:
            new_follower = FollowerModel(
                follower_id = json.get("followerId"),
                user_id = json.get("userId"),
                accepted = json.get("followerAccepted")
            )
            db.session.add(new_follower)
            db.session.commit()
            return {"message": "Follower added."}
        except ValueError as e:
            return {"error": [str(e)]}