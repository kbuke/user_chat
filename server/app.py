from config import api, app

from resources.User import UserList

api.add_resource(UserList, "/users")

if __name__ == "__main__":
    app.run(port = 5555, debug = True)