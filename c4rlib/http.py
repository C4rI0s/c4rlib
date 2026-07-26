import json
import random
import urllib.request
import urllib.parse
import urllib.error
import ssl


class Response:
    def __init__(self, status: int, headers: dict, body: bytes, url: str):
        self.status  = status
        self.headers = headers
        self.url     = url
        self._body   = body

    @property
    def text(self) -> str:
        return self._body.decode("utf-8", errors="replace")

    @property
    def content(self) -> bytes:
        return self._body

    def json(self) -> dict:
        return json.loads(self.text)

    def ok(self) -> bool:
        return 200 <= self.status < 300

    def __repr__(self) -> str:
        return f"<Response [{self.status}] {self.url}>"


class Http:
    _DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/html, */*",
        "Accept-Language": "en-US,en;q=0.9",
    }

    @staticmethod
    def _make_ctx(verify_ssl: bool = True):
        if not verify_ssl:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode    = ssl.CERT_NONE
            return ctx
        return None

    @staticmethod
    def get(url: str, params: dict = None, headers: dict = None,
            timeout: int = 10, verify_ssl: bool = True, proxy: str = None) -> Response:
        if params:
            url = url + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url)
        merged = {**Http._DEFAULT_HEADERS, **(headers or {})}
        for k, v in merged.items():
            req.add_header(k, v)
        if proxy:
            req.set_proxy(proxy, "http")
        ctx = Http._make_ctx(verify_ssl)
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return Response(r.status, dict(r.headers), r.read(), url)

    @staticmethod
    def post(url: str, data: dict = None, json_data: dict = None,
             headers: dict = None, timeout: int = 10, verify_ssl: bool = True) -> Response:
        merged = {**Http._DEFAULT_HEADERS, **(headers or {})}
        if json_data is not None:
            body = json.dumps(json_data).encode()
            merged["Content-Type"] = "application/json"
        elif data is not None:
            body = urllib.parse.urlencode(data).encode()
            merged["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            body = b""
        req = urllib.request.Request(url, data=body, method="POST")
        for k, v in merged.items():
            req.add_header(k, v)
        ctx = Http._make_ctx(verify_ssl)
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return Response(r.status, dict(r.headers), r.read(), url)

    @staticmethod
    def put(url: str, json_data: dict = None, headers: dict = None,
            timeout: int = 10, verify_ssl: bool = True) -> Response:
        merged = {**Http._DEFAULT_HEADERS, **(headers or {})}
        body   = json.dumps(json_data or {}).encode()
        merged["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=body, method="PUT")
        for k, v in merged.items():
            req.add_header(k, v)
        ctx = Http._make_ctx(verify_ssl)
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return Response(r.status, dict(r.headers), r.read(), url)

    @staticmethod
    def delete(url: str, headers: dict = None,
               timeout: int = 10, verify_ssl: bool = True) -> Response:
        merged = {**Http._DEFAULT_HEADERS, **(headers or {})}
        req    = urllib.request.Request(url, method="DELETE")
        for k, v in merged.items():
            req.add_header(k, v)
        ctx = Http._make_ctx(verify_ssl)
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return Response(r.status, dict(r.headers), r.read(), url)

    @staticmethod
    def patch(url: str, json_data: dict = None, headers: dict = None,
              timeout: int = 10, verify_ssl: bool = True) -> Response:
        merged = {**Http._DEFAULT_HEADERS, **(headers or {})}
        body   = json.dumps(json_data or {}).encode()
        merged["Content-Type"] = "application/json"
        req    = urllib.request.Request(url, data=body, method="PATCH")
        for k, v in merged.items():
            req.add_header(k, v)
        ctx = Http._make_ctx(verify_ssl)
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return Response(r.status, dict(r.headers), r.read(), url)

    @staticmethod
    def head(url: str, headers: dict = None, timeout: int = 10) -> Response:
        merged = {**Http._DEFAULT_HEADERS, **(headers or {})}
        req    = urllib.request.Request(url, method="HEAD")
        for k, v in merged.items():
            req.add_header(k, v)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return Response(r.status, dict(r.headers), b"", url)

    @staticmethod
    def download(url: str, path: str, headers: dict = None, timeout: int = 30) -> int:
        merged = {**Http._DEFAULT_HEADERS, **(headers or {})}
        req    = urllib.request.Request(url)
        for k, v in merged.items():
            req.add_header(k, v)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
        with open(path, "wb") as f:
            f.write(data)
        return len(data)

    @staticmethod
    def build_headers(token: str = None, content_type: str = None,
                      user_agent: str = None, extra: dict = None) -> dict:
        headers = {}
        if token:        headers["Authorization"] = f"Bearer {token}"
        if content_type: headers["Content-Type"]  = content_type
        if user_agent:   headers["User-Agent"]     = user_agent
        if extra:        headers.update(extra)
        return headers

    @staticmethod
    def random_headers(token: str = None) -> dict:
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        ]
        headers = {
            "User-Agent":      random.choice(agents),
            "Accept":          "application/json, text/html, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection":      "keep-alive",
            "Sec-Fetch-Site":  "none",
            "Sec-Fetch-Mode":  "navigate",
        }
        if token: headers["Authorization"] = f"Bearer {token}"
        return headers

    @staticmethod
    def parse_url(url: str) -> dict:
        parsed = urllib.parse.urlparse(url)
        return {
            "scheme":   parsed.scheme,
            "host":     parsed.netloc,
            "path":     parsed.path,
            "query":    dict(urllib.parse.parse_qsl(parsed.query)),
            "fragment": parsed.fragment,
        }

    @staticmethod
    def encode_params(params: dict) -> str:
        return urllib.parse.urlencode(params)

    @staticmethod
    def build_url(base: str, path: str = "", params: dict = None) -> str:
        url = base.rstrip("/") + ("/" + path.lstrip("/") if path else "")
        if params: url += "?" + urllib.parse.urlencode(params)
        return url

    @staticmethod
    def is_reachable(url: str, timeout: int = 5) -> bool:
        try:
            Http.head(url, timeout=timeout)
            return True
        except Exception:
            return False
