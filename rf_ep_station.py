import http.server
import json
import math
import random
import struct
import time

class RFEPStreamHandler(http.server.BaseHTTPRequestHandler):
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
                    chunk = bytearray()
                    # Generate 100ms multi-layered telemetry buffer
                    for _ in range(sample_rate // 10):
                        # 1. RF Noise Floor (RSSI static proportional to signal strength)
                        rssi_noise = (random.random() * 2.0 - 1.0) * 4000
                        
                        # 2. BCI Evoked Potential (EP) Click Train / Impulse Stimulus every 50ms
                        ep_click = 12000 if int(t * 1000) % 50 < 4 else 0
                        
                        # 3. Harmonic Resonance & Chamber AI Carrier Frequency Modulation
                        polarity = math.sin(t * 2.0)
                        carrier = math.sin(2 * math.pi * (180.0 + polarity * 60.0) * t) * 8000
                        sub_harmonic = math.cos(2 * math.pi * 45.0 * t) * 4000
                        
                        # Composite sample mixing RF noise, EP clicks, and neural harmonics
                        sample = rssi_noise + ep_click + carrier + sub_harmonic
                        sample = max(min(sample, 32767), -32768)
                        
                        chunk.extend(struct.pack('<h', int(sample)))
                        t += 1.0 / sample_rate
                        
                    self.wfile.write(f"{len(chunk):X}\r\n".encode('utf-8'))
                    self.wfile.write(chunk + b"\r\n")
                    self.wfile.flush()
                    time.sleep(0.08)
            except (ConnectionError, BrokenPipeError):
                pass
                
        elif clean_path == "/station/telemetry":
            t = time.time()
            payload = {
                "resource_id": "BCI-RF-NODE-01",
                "position_enu_m": [6.0, 4.0, 2.0],
                "rf": {
                    "mode": "EP_TELEMETRY_RX",
                    "frequency_hz": 2400000000,
                    "bandwidth_hz": 4000000,
                    "telemetry": {
                        "rssi_dbm": round(-64.2 + (random.random() * 2.0 - 1.0), 2),
                        "snr_db": 21.8,
                        "evoked_potential_latency_ms": 14.2
                    }
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
    server = http.server.HTTPServer(("127.0.0.1", 8080), RFEPStreamHandler)
    print("[RF + EP AUDIO STATION ACTIVE] Stream running at http://127.0.0.1:8080/station/audio")
    server.serve_forever()
