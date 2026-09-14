import http.server
import json
import math
import random
import time

class RFStationHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        clean_path = self.path.rstrip('/')
        t = time.time()
        polarity_vector = math.sin(t * 0.5)
        rssi_val = -65.0 + (random.random() * 4.0 - 2.0)
        echo_resonance = round(math.cos(t * 0.25) * 48.2, 2)
        
        if clean_path == "/station/telemetry":
            payload = {
                "resource_id": "RF-STATION-POLARITY-01",
                "position_enu_m": [6.0, 4.0, 2.0],
                "rf": {
                    "mode": "RX_TX_RESONATE",
                    "frequency_hz": 2400000000,
                    "bandwidth_hz": 2000000,
                    "antenna_id": "ANT-POLARITY-01",
                    "telemetry": {
                        "rssi_dbm": round(rssi_val, 2),
                        "snr_db": 19.4,
                        "polarity_source_state": round(polarity_vector, 4)
                    }
                },
                "chamber_ai_model": {
                    "origin_generator": "MAGNET_RESONATE_ACTIVE",
                    "echo_field_ut": echo_resonance,
                    "inference_status": "LOCKED_SYNCHRONIZED"
                },
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "station endpoint not found"}')

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    server = http.server.HTTPServer(("127.0.0.1", 8080), RFStationHandler)
    print("[RF STATION ACTIVE] Polarity & Echo Stream online at http://127.0.0.1:8080/station/telemetry")
    
    import threading
    def serve():
        server.serve_forever()
        
    t_server = threading.Thread(target=serve, daemon=True)
    t_server.start()

    try:
        while True:
            t = time.time()
            pol = round(math.sin(t * 0.5), 2)
            rssi = round(-65.0 + (random.random() * 4.0 - 2.0), 1)
            echo = round(math.cos(t * 0.25) * 48.2, 1)
            print(f"[CHAMBER AI SYNC] Polarity: {pol:+0.2f} | RSSI: {rssi} dBm | Echo Resonate: {echo} uT")
            time.sleep(1.5)
    except KeyboardInterrupt:
        print("\n[RF STATION] Shutdown sequence initiated.")
