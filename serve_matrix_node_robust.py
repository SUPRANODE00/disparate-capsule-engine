import http.server
import socketserver
import os

PORT = 8080
DIRECTORY = "DECLINED_AT_BIRTH_MATRIX"

if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)
    with open(os.path.join(DIRECTORY, "index.html"), "w") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>DECLINED AT BIRTH MATRIX | D3M13N CAPSULECRAFT</title>
    <style>
        body { background-color: #050505; color: #00ff66; font-family: monospace; padding: 40px; }
        h1 { border-bottom: 1px solid #00ff66; padding-bottom: 10px; }
        .node-box { border: 1px solid #00ff66; padding: 20px; margin-top: 20px; background: #0a0a0a; }
    </style>
</head>
<body>
    <h1>DECLINED AT BIRTH MATRIX // D3M13N CAPSULECRAFT</h1>
    <div class="node-box">
        <p>STATUS: ACTIVE & SECURED</p>
        <p>JURISDICTION: Harris County / Southern District, Houston Division</p>
        <p>MESH TELEMETRY: LOCKED</p>
    </div>
</body>
</html>""")

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

with ReusableTCPServer(("", PORT), Handler) as httpd:
    print(f"[+] Serving D3M13N CAPSULECRAFT matrix node on port {PORT}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[+] Server shutdown cleanly.")
