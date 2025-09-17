from config import db
from models.IndividualChat import IndividualChatModel
from flask import request
from flask_restful import Resource

class IndividualChatList(Resource):
    def get(self):
        individual_chats = [chat.to_dict() for chat in IndividualChatModel.query.all()]
        return individual_chats
    
    def post(self):
        json = request.get_json()
        try:
            new_chat = IndividualChatModel.create_chat(
                json.get("userId"),
                json.get("otherUserId")
            )
            db.session.add(new_chat)
            db.session.commit()
            return {"message": "New chat added"}
        except (ValueError, PermissionError) as e:
            return {"error": [str(e)]}

class IndividualChat(Resource):
    def get(self, id):
        chat = IndividualChatModel.query.filter(IndividualChatModel.id == id).first()
        if chat:
            return chat.to_dict(), 201
        else:
            return {"error": f"Chat {id} not found"}, 404
        
    def delete(self, id):
        chat = IndividualChatModel.query.filter(IndividualChatModel.id == id).first()
        if chat:
            db.session.delete(chat)
            db.session.commit()
            return {"message": f"Chat {id} deleted"}, 201
        else:
            return {"error": f"Chat {id} not registered"}, 404