# structures.py
from microhttpx.structs import HttpxStruct, HttpxField
from microhttpx.request import HttpxRequest
from microhttpx.server import HttpxServer

class GetUsersStruct(HttpxStruct):
    __route__ = "/users/{uuid}"
    __fields__ = {
        "uuid": HttpxField(str, required=True),
        "expand": HttpxField(str, required=False, default="basic"),
    }

    uuid: str
    expand: str

# main.py
server = HttpxServer()

@server.route("/users/{uuid}")
def get_user(req:HttpxRequest):
    try:
        user = GetUsersStruct(req)
    except ValueError as e:
        return {"error": str(e)}

    return {
        "uuid": user.uuid,
        "expand": user.expand
    }
