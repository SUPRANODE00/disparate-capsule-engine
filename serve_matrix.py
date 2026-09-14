import os, http.server, socketserver, json, time

PORT = 8080
DIRECTORY = "DECLINED_AT_BIRTH_MATRIX"
os.makedirs(DIRECTORY, exist_ok=True)

with open(os.path.join(DIRECTORY, "index.html"), "w") as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
  <head><meta charset="utf-8" /><title>D3M13N CAPSULECRAFT</title></head>
  <body style="background:#050505; color:#00ff66; font-family:monospace; padding:40px;">
    <h2>MESH TELEMETRY & VECTOR MAPPING MATRIX</h2>
    <p><strong>STATUS:</strong> ACTIVE & SECURED</p>
    <p><strong>DBA:</strong> D3M13N CAPSULECRAFT</p>
    <p><strong>JURISDICTION:</strong> Harris County / Southern District, Houston Division</p>
  </body>
</html>""")

class MatrixHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    def do_GET(self):
        if self.path == "/telemetry":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            telemetry = {
                "resource_id": "RF-NODE-D3M13N-BEDROCKMAP",
                "dba": "D3M13N CAPSULECRAFT",
                "jurisdiction": "Harris County / Southern District, Houston Division",
                "spatial_enu": [6.0, 4.0, 2.0],
                "rf": {"mode": "TX/RX", "frequency_hz": 2400000000, "rssi_dbm": -67},
                "status": "BEDROCKMAP_MESH_SYNCHRONIZED",
                "timestamp": int(time.time())
            }
            self.wfile.write(json.dumps(telemetry, indent=2).encode('utf-8'))
        else:
            super().do_GET()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), MatrixHandler) as httpd:
    print(f"[+] Serving D3M13N CAPSULECRAFT matrix node on port {PORT}...")
    httpd.serve_forever()
