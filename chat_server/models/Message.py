from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from config import db
from models.User import UserModel
from models.IndividualChat import IndividualChatModel

class MessageModel(db.Model, SerializerMixin):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.ForeignKey("users.id"))
    user = db.relationship(
        "UserModel",
        back_populates = "messages"
    )

    chat_id = db.Column(db.ForeignKey("individual_chats.id"))
    chat = db.relationship(
        "IndividualChatModel",
        back_populates = "messages",
    )

    content = db.Column(db.String, nullable = False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @validates("content")
    def validate_message_content(self, key, value):
        if not isinstance(value, str):
            raise ValueError("Message content must be a string")
        
        if value is None or value == "":
            raise ValueError("Please enter a valid input")
        
        return value
        
    @validates("user_id")
    def validate_user(self, key, value):
        if not isinstance(value, int):
            raise ValueError("user id must be an integer.")
        
        if isinstance(value, int):
            existing_user = UserModel.query.filter(UserModel.id == value).first()
            if not existing_user:
                raise ValueError(f"No user {value} found")
        
        return value
    
    @validates("chat_id")
    def validate_chat(self, key, value):
        if not isinstance(value, int):
            raise ValueError("chat id must be an integer")
        
        if isinstance(value, int):
            existing_chat = IndividualChatModel.query.filter(IndividualChatModel.id == value).first()
            if not existing_chat:
                raise ValueError(f"No chat {value} found")
        
        return value