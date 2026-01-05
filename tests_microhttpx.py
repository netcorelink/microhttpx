from microhttpx.structs import HttpxField, HttpxStruct
from microhttpx.parser import HttpxParser
import time

def run_test(fn):
    start=time.perf_counter()
    fn()
    duration=(time.perf_counter()-start)*1000
    print(f"[OK] {fn.__name__} ({duration:.2f} ms)")

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

def test_parser_query_empty():
    assert HttpxParser.query("/test") == {}

def test_parser_body():
    body="a=1&b=hello"
    params=HttpxParser.body(body)

    assert params["a"]=="1"
    assert params["b"]=="hello"

def test_parser_body_empty():
    assert HttpxParser.body("") == {}

def test_parser_path_params():
    route="/users/{uuid}"
    path="/users/abc-123"

    params=HttpxParser.path_params(route, path)

    assert params["uuid"]=="abc-123"

def test_parser_path_params_mismatch():
    assert HttpxParser.path_params("/users/{id}", "/posts/1") is None

def test_struct_ok():
    req=HttpxMockReq("/users/42?page=3")
    user=UserStruct(req)

    assert user.id=="42"
    assert user.page==3

def test_struct_default():
    req = HttpxMockReq("/users/42")
    user = UserStruct(req)

    assert user.page == 1

def test_struct_required_fail():
    try:
        req=HttpxMockReq("/users/")
        UserStruct(req)

        raise Exception("required check failed")
    except ValueError:
        print("[OK] test_struct_required_fail")

def test_struct_type_fail():
    try:
        UserStruct(HttpxMockReq("/users/42?page=abc"))
        assert False, "type validation not detected"
    except ValueError:
        pass

if __name__=="__main__":
    tests = [
        test_parser_query,
        test_parser_query_empty,
        test_parser_body,
        test_parser_body_empty,
        test_parser_path_params,
        test_parser_path_params_mismatch,
        test_struct_ok,
        test_struct_default,
        test_struct_required_fail,
        test_struct_type_fail,
    ]

    start_all = time.perf_counter()

    for t in tests:
        run_test(t)

    total = (time.perf_counter() - start_all) * 1000
    print(f"\n== ALL TESTS PASSED ({total:.2f} ms) ==")
