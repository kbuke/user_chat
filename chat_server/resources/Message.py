from models.Message import MessageModel
from config import db
from flask import request
from flask_restful import Resource

class MessageList(Resource):
    def get(self):
        messages = [message.to_dict() for message in MessageModel.query.all()]
        return messages, 201
    
    def post(self):
        json = request.get_json()
        try:
            new_message = MessageModel(
                user_id = json.get("userId"),
                chat_id = json.get("chatId"),
                content = json.get("messageContent")
            )
            db.session.add(new_message)
            db.session.commit()
            return {"message": "New message posted"}
        except ValueError as e:
            return {"error": [str(e)]}, 400

class Message(Resource):
    def get(self, id):
        message = MessageModel.query.filter(MessageModel.id == id).first()
        if message:
            return message.to_dict(), 201
    
    def delete(self, id):
        message = MessageModel.query.filter(MessageModel.id == id).first()
        if message:
            db.session.delete(message)
            db.session.commit()
            return {"message": f"Message {id} deleted"}, 201
        else:
            return {"error": f"Message {id} not found"}, 404