from microhttpx import HttpxServer, HttpxRequest, HttpxStruct, HttpxField

class GetUsersStruct(HttpxStruct):
    __route__ = "/users/{uuid}"
    __fields__ = {
        "uuid": HttpxField(str, required=True),
        "expand": HttpxField(str, required=False, default="basic"),
    }

    uuid: str
    expand: str

server = HttpxServer()

@server.route("/users/{uuid}")
def get_user(req: HttpxRequest):
    try:
        user = GetUsersStruct(req)
    except ValueError as e:
        return {"error": str(e)}

    return {
        "uuid": user.uuid,
        "expand": user.expand
    }

server.listen(port=8080)
