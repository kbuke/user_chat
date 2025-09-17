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

class Follower(Resource):
    def delete(self, id):
        follow = FollowerModel.query.filter(FollowerModel.id == id).first()
        if follow:
            db.session.delete(follow)
            db.session.commit()
            return {"message": f"Follow relationship {id} deleted"}, 201
        else:
            return {"error": f"No follow relationship {id} registered here"}, 404