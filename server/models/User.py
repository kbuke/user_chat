# Create the User Model
    # Keep simple. User should have following attributes
        # Username <string>
        # Password <string>
        # Profile Picture <string with a dafault value>
        # Gender (which will determine the default profile pic)
        # Open to all messages <Boolean>

    # Should have following relations
        # Relation with chats (a user can be part of many chats, and many chats can belong to a user)
        # Followers and Following

from config import db, bcrypt
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin


class UserModel(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    gender = db.Column(db.String, nullable = False)
    profile_picture = db.Column(db.String)
    allow_all_messages = db.Column(db.Boolean)
    _password_hash = db.Column(db.String, nullable = False)

    # RELATIONS
    # followers - a user can have many followers, and a follower can follow many users
    followers = db.relationship(
        "FollowerModel", 
        foreign_keys="FollowerModel.user_id", 
        backref = "followed_user", 
        cascade="all, delete-orphan"
    )

    # following - a follower can follow many users, and a user can have many followers
    following = db.relationship(
        "FollowerModel",
        foreign_keys = "FollowerModel.follower_id",
        backref = "following_user",
        cascade = "all, delete-orphan"
    )

    # SERIALIZE RULES
    serialize_rules = (
        "-followers.followed_user",
        "-followers.following_user",
        
        "-following.followed_user",
        "-following.following_user",
    )

    # hash the password
    @hybrid_property
    def password_hash(self):
        raise AttributeError("password: write-only attribute")
    
    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    # VALIDATIONS
    # validate user name
    @validates("username")
    def validate_username(self, key, value):
        if not isinstance (value, str):
            raise ValueError("Username must be a string")
        
        if value is None or value == "":
            raise ValueError("Please enter a valid username")
        
        new_username = value if key == "username" else self.username
        existing_name = UserModel.query.filter(UserModel.username == new_username).first()
        if existing_name and existing_name.id != self.id:
            raise ValueError(f"{value} is already registered")
        
        return value
    
    #validate profile picture based on users gender
    @validates("gender", "profile_picture")
    def validate_gender_and_picture(self, key, value):
        allowed_genders = ["Male", "Female", "Other"]

        if key == "gender" and value not in allowed_genders:
            raise ValueError("User gender must either be Male, Female or Other")
        
        if key == "profile_picture" and (value is None or value == ""):
            if self.gender == "Male":
                value = "https://static.vecteezy.com/system/resources/previews/024/183/525/non_2x/avatar-of-a-man-portrait-of-a-young-guy-illustration-of-male-character-in-modern-color-style-vector.jpg"
            elif self.gender == "Female":
                value = "https://t4.ftcdn.net/jpg/11/66/06/77/360_F_1166067709_2SooAuPWXp20XkGev7oOT7nuK1VThCsN.jpg"
            else:
                value = "https://img.freepik.com/free-photo/androgynous-avatar-non-binary-queer-person_23-2151100270.jpg"
        
        return value
