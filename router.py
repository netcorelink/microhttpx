from httpx.request import Request
from httpx.response import Response
from httpx.status import StatusNotFound
import socket

class Router:
    def __init__(self):
        self.routes=[]

    def get(self, path, handler):
        self.routes.append(("GET", path, handler))

    def post(self, path, handler):
        self.routes.append(("POST", path, handler))

    def handle(self, conn: socket, raw):
        req=Request(raw)

        for m, p, h in self.routes:
            if m == req.method and p == req.path:
                return h(conn, req)

        Response.resp(conn, StatusNotFound())
