from config import api, app

from resources.User import UserList

from resources.Followers import FollowersList

api.add_resource(UserList, "/users")

api.add_resource(FollowersList, "/followers")

if __name__ == "__main__":
    app.run(port = 5555, debug = True)