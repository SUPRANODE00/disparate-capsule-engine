import http.server
import json
import socketserver
import threading
import time
import subprocess

class SatelliteUSSDHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        try:
            req = json.loads(post_data.decode('utf-8'))
        except Exception:
            req = {}

        dial_string = req.get("dial_string", "")
        response_payload = {}

        if dial_string == "*#*#1234*#*#":
            response_payload = {
                "ingress_ack": "SUCCESS",
                "satellite_link": "ESTABLISHED_GEO_ORBIT_SL1TH3R_00",
                "sim_signal_routing": "ACTIVE",
                "mcc_mnc": "310/410",
                "carrier": "cricket (us)",
                "cell_ipv6": "2600:381:459b:be88:3179:f1c6:11f3:1fd5/64",
                "gateway_bridge": "fe80::7",
                "telemetry_status": "LIVE_AUDIO_RF_HOPPING_LOCKED",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            self.send_response(200)
        else:
            response_payload = {
                "ingress_ack": "REJECTED_INVALID_USSD",
                "dial_string_received": dial_string,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            self.send_response(400)

        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_payload, indent=2).encode("utf-8"))

    def do_GET(self):
        if self.path.rstrip('/') == "/satellite/status":
            payload = {
                "satellite_bot": "CAPSULECRAFT-SAT-BOT-01",
                "egress_ingress_ack_agent": "ONLINE",
                "active_sim_interface": "CELLULAR_GSM_READY",
                "supported_ussd": "*#*#1234*#*#",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer(("127.0.0.1", 8080), SatelliteUSSDHandler)
    print("[SATELLITE-BOT USSD INGRESS AGENT ACTIVE] Listening on port 8080 for *#*#1234*#*# sequence")
    server.serve_forever()
