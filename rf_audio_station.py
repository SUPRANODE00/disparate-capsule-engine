import http.server
import json
import math
import random
import struct
import time

class RFAudioStreamHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        clean_path = self.path.rstrip('/')
        
        if clean_path == "/station/audio":
            self.send_response(200)
            self.send_header("Content-Type", "audio/x-raw")
            self.send_header("Transfer-Encoding", "chunked")
            self.end_headers()
            
            sample_rate = 8000
            t = 0.0
            try:
                while True:
                    # RF parameter modulation: RSSI and polarity vector state driving frequency
                    rssi_mod = -65.0 + (random.random() * 4.0 - 2.0)
                    polarity = math.sin(t * 0.5)
                    freq = 440.0 + (polarity * 220.0) + ((rssi_mod + 65.0) * 10.0)
                    
                    chunk = bytearray()
                    for _ in range(sample_rate // 10):
                        sample = math.sin(2 * math.pi * freq * t) * 16383
                        chunk.extend(struct.pack('<h', int(sample)))
                        t += 1.0 / sample_rate
                        
                    self.wfile.write(f"{len(chunk):X}\r\n".encode('utf-8'))
                    self.wfile.write(chunk + b"\r\n")
                    self.wfile.flush()
                    time.sleep(0.1)
            except (ConnectionError, BrokenPipeError):
                pass
                
        elif clean_path == "/station/telemetry":
            t = time.time()
            payload = {
                "resource_id": "RF-STATION-POLARITY-01",
                "position_enu_m": [6.0, 4.0, 2.0],
                "rf": {
                    "mode": "RX_TX_RESONATE",
                    "frequency_hz": 2400000000,
                    "bandwidth_hz": 2000000,
                    "antenna_id": "ANT-POLARITY-01",
                    "telemetry": {
                        "rssi_dbm": round(-65.0 + (random.random() * 4.0 - 2.0), 2),
                        "snr_db": 19.4,
                        "polarity_source_state": round(math.sin(t * 0.5), 4)
                    }
                },
                "chamber_ai_model": {
                    "origin_generator": "MAGNET_RESONATE_ACTIVE",
                    "echo_field_ut": round(math.cos(t * 0.25) * 48.2, 2),
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
            self.wfile.write(b'not found')

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    server = http.server.HTTPServer(("127.0.0.1", 8080), RFAudioStreamHandler)
    print("[RF AUDIO STATION ACTIVE] Connect stream player to http://127.0.0.1:8080/station/audio")
    server.serve_forever()
