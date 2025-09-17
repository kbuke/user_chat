from config import db
from sqlalchemy_serializer import SerializerMixin

from models.User import UserModel

from sqlalchemy.orm import validates

class FollowerModel(db.Model, SerializerMixin):
    __tablename__ = "followers"

    id = db.Column(db.Integer, primary_key = True)
    follower_id = db.Column(db.ForeignKey("users.id"))
    user_id = db.Column(db.ForeignKey("users.id"))
    accepted = db.Column(db.Boolean, default = False)

    @validates("follower_id", "user_id")
    def validate_user_ids(self, key, value):

        # 1 - ID must be an integer
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError:
                raise ValueError("Id must be an integer value.")
        
        # 2 - ID must belong to a user registered on app
        existing_user = UserModel.query.filter(UserModel.id == value).first()
        if not existing_user:
            raise ValueError(f"User {value} is not registered on this app.")
        
        # 3 - Ensure the user can not follow themselves
        other_value = self.user_id if key == "follower_id" else self.follower_id
        if other_value and value == other_value:
            raise ValueError("A user can not follow themselves.")
        
        # 4 - Check if the relationship exists
        user_id = value if key == "user_id" else self.user_id
        follower_id = value if key == "follower_id" else self.follower_id

        if user_id and follower_id:
            existing_relationship = FollowerModel.query.filter_by(
                user_id = user_id,
                follower_id = follower_id
            ).first()

            if existing_relationship:
                raise ValueError("This follow relationship already exists")
            
        return value
    
    @validates("accepted")
    def validate_follow_request(self, key, value):
        # 1 - Check the logged in user is the user who's been sent a follow request

        # 2 - Check the value is a boolean
        if not isinstance(value, bool):
            raise ValueError("Value of accept must be a boolean")
        
        # 3 - If value is false the request is rejected.
        if value is False:
            raise ValueError("The follow request was rejected.")
        
        return value