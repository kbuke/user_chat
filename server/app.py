from config import api, app

from resources.User import UserList, User

from resources.Followers import FollowersList

from resources.IndividualChat import IndividualChatList, IndividualChat

api.add_resource(UserList, "/users")
api.add_resource(User, "/users/<int:id>")

api.add_resource(FollowersList, "/followers")

api.add_resource(IndividualChatList, "/individualchats")
api.add_resource(IndividualChat, "/individualchats/<int:id>")

if __name__ == "__main__":
    app.run(port = 5555, debug = True)