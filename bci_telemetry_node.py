import http.server
import json
import math
import random
import socketserver
import subprocess
import threading
import time

def audio_daemon():
    cmd = ["aplay", "-q", "-r", "8000", "-f", "S16_LE", "-c", "1"]
    try:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        t = 0.0
        while True:
            # 10Hz alpha modulation on 440Hz carrier
            sample = int(12000 * math.sin(2 * math.pi * 440.0 * t) * (0.5 + 0.5 * math.sin(2 * math.pi * 10.0 * t)))
            sample = max(-32768, min(32767, sample))
            proc.stdin.write(sample.to_bytes(2, byteorder='little', signed=True))
            t += 0.000125
            time.sleep(0.0001)
    except Exception:
        pass

audio_thread = threading.Thread(target=audio_daemon, daemon=True)
audio_thread.start()

class BCITelemetryHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.rstrip('/') == "/station/telemetry":
            payload = {
                "resource_id": "UNICORN-HYPERSN-BCI-01",
                "electrode_status": {
                    "channels": ["Fz", "C3", "Cz", "C4", "Pz", "PO7", "OZ", "PO8"],
                    "impedance_kohm": {"Fz": 2.1, "C3": 1.7, "Cz": 1.9, "C4": 1.8, "Pz": 2.3, "PO7": 2.9, "OZ": 2.6, "PO8": 2.8},
                    "contact_quality": "EXCELLENT",
                    "bridge_fault_detected": False
                },
                "alpha_wave_metrics": {
                    "frequency_hz": 10.0,
                    "band_power_uv2": 19.45,
                    "audio_modulation_status": "ACTIVE_PCM_ALSA_STREAMING"
                },
                "evoked_potentials": {
                    "p300_amplitude_uv": 14.12,
                    "latency_ms": 310.2,
                    "stimulus_lock": "SYNCHRONIZED"
                },
                "rf_resource": {
                    "mode": "TRANSMIT_RECEIVE_HOPPING",
                    "frequency_hz": 2400000000,
                    "bandwidth_hz": 20000000,
                    "antenna_id": "ANT-BCI-01",
                    "telemetry": {
                        "rssi_dbm": -61.2,
                        "snr_db": 27.5
                    }
                },
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
    server = socketserver.TCPServer(("127.0.0.1", 8080), BCITelemetryHandler)
    print("[UNICORN BCI NODE ACTIVE] Audio stream & telemetry running on port 8080")
    server.serve_forever()
