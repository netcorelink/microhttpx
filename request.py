class Request:
    def __init__(self, raw:str):
        self.raw=raw
        self.method=None
        self.path=None
        self.headers={}
        self.body=""
        self.params={}

        self._parse()

    def _parse(self):
        head, body=self.raw.split("\r\n\r\n", 1)
        lines=head.split("\r\n")

        self.method, self.path, _ = lines[0].split(" ")

        # Headers
        for line in lines[1:]:
            if ":" in line:
                k, v = line.split(":", 1)
                self.headers[k.strip()] = v.strip()

        self.body=body

        if body:
            try:
                for param in body.split("&"):
                    k, v = param.split("=", 1)
                    self.params[k] = v
            except:
                pass
