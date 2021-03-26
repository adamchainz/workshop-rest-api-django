from wsgiref.simple_server import make_server


def hello_world_app(environ, start_response):
    status = "200 OK"
    headers = [("Content-type", "text/html; charset=utf-8")]
    body = [b"<h1>Hello World</h1>\n"]
    start_response(status, headers)

    return body


with make_server("", 8000, hello_world_app) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
