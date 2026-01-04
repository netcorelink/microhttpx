from microhttpx.parser import HttpxParser
from microhttpx.server import HttpxServer
from microhttpx.structs import HttpxField, HttpxStruct

class UserStruct(HttpxStruct):
    __route__ = "/users/{id}"
    __fields__ = {
        "id": HttpxField(str, required=True),
        "page": HttpxField(int, default=1),
    }

    id: str
    page: int

class HttpxMockReq:
    def __init__(self, path="/", body="", method="GET"):
        self.path = path
        self.body = body
        self.method = method
        self.headers = {}
        self.conn = None

def test_parser_query():
    req="/test?name=netcorelink&project=microhttpx"
    params=HttpxParser.query(req)

    assert params["name"] == "netcorelink"
    assert params["project"] == "microhttpx"

    print("[OK] test_parser_query")

def test_parser_body():
    body="a=1&b=hello"
    params=HttpxParser.body(body)

    assert params["a"]=="1"
    assert params["b"]=="hello"

    print("[OK] test_parser_body")

def test_parser_path_params():
    route="/users/{uuid}"
    path="/users/abc-123"

    params=HttpxParser.path_params(route, path)

    assert params["uuid"]=="abc-123"

    print("[OK] test_parser_path_params")

def test_struct():
    req=HttpxMockReq("/users/42?page=3")
    user=UserStruct(req)

    assert user.id=="42"
    assert user.page==3

    print("[OK] test_struct")

def test_struct_required_fail():
    try:
        req=HttpxMockReq("/users/")
        UserStruct(req)

        raise Exception("required check failed")
    except ValueError:
        print("[OK] test_struct_required_fail")

if __name__=="__main__":
    test_parser_query()
    test_parser_body()
    test_parser_path_params()
    test_struct()
    test_struct_required_fail()

    print("== ALL TESTS PASSED ==")
