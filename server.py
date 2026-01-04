from httpx.router import Router
from module.logger_module import Logger
import socket

class Server:
    def __init__(self, router:Router, port:str="80"):
        self.port=port
        self.sock=socket.socket()
        self.sock.bind(("", port))
        self.sock.listen(1)
        self.router=router

    def listen(self):
        Logger.log("SERV", "http server started on port {}".format(self.port))

        while True:
            conn, _ = self.sock.accept()

            try:
                req = conn.recv(1024).decode()
                self.router.handle(conn, req)
            except Exception as e:
                Logger.error("SERV", e)
            finally:
                conn.close()
