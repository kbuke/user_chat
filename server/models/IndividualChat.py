# The individual chat belongs to 2 users.
# The chat will have many messages

from config import db
from sqlalchemy import UniqueConstraint, inspect
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from models.User import UserModel

class IndividualChatModel(db.Model, SerializerMixin):
    __tablename__ = "individual_chats"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.ForeignKey("users.id"))
    other_user_id = db.Column(db.ForeignKey("users.id"))

    __table_args__ = (
        UniqueConstraint("user_id", "other_user_id", name = "unique_chat_pair"),
    )

    serialize_rules = (
        "-starter",
        "-receiver",
    )

    # VALIDATIONS
    @validates("user_id", "other_user_id")
    def validate_chat_users(self, key, value):
        # Ensure integer
        if not isinstance(value, int):
            raise ValueError("IDs must be integers.")

        # Grab the raw value of the "other" column without triggering SQLAlchemy instrumentation
        state = inspect(self)
        dict_ = state.dict  # raw attribute dictionary

        other = dict_.get("other_user_id") if key == "user_id" else dict_.get("user_id")

        if other is not None:
            low, high = sorted([value, other])
            return low if key == "user_id" else high

        return value


    @classmethod
    def create_chat(cls, user_a_id, user_b_id):
        if user_a_id == user_b_id:
            raise ValueError("A user can not chat with themselves")
    
        low, high = sorted([user_a_id, user_b_id])

        existing = cls.query.filter_by(user_id = low, other_user_id = high).first()
        if existing:
            raise ValueError("Chat already exists")
        
        user_a = UserModel.query.get(user_a_id)
        user_b = UserModel.query.get(user_b_id)

        if not user_a or not user_b:
            raise ValueError("Both users must be registered in the app.")
        
        def can_receive(sender, receiver):
            if receiver.allow_all_messages:
                return True
            return any(f.follower_id == sender.id for f in receiver.followers)
        
        if not (can_receive(user_a, user_b) and can_receive(user_b, user_a)):
            raise PermissionError("Users can not start a conversation")
        
        chat = cls(user_id = low, other_user_id = high)
        db.session.add(chat)
        db.session.commit()
        return chat