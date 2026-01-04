import socket

class Response:
    @staticmethod
    def resp(conn:socket, status:str, body="", content_type="text/plain"):
        conn.send(
            "HTTP/1.1 {}\r\n"
            "Content-Type: {}\r\n"
            "Content-Length: {}\r\n\r\n"
            .format(status, content_type, len(body))
        )

        if body: conn.send(body)

    @staticmethod
    def json(conn: socket, status: str, payload):
        Response.resp(conn, status, payload, "application/json")

    @staticmethod
    def html(conn: socket, status: str, html):
        Response.resp(conn, status, html, "text/html")
