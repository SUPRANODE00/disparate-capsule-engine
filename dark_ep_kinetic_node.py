import http.server
import json
import math
import random
import socketserver
import time

class DarkEPKineticHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        clean_path = self.path.rstrip('/')
        
        if clean_path == "/station/telemetry":
            t = time.time()
            payload = {
                "resource_id": "SUPRANODE-DARK-EP-KINETIC-01",
                "position_enu_m": [6.0, 4.0, 2.0],
                "geo_pose": {
                    "latitude": 29.7604,
                    "longitude": -95.3698,
                    "altitude_m": 12.5,
                    "heading_deg": 142.5
                },
                "rf_resource": {
                    "mode": "DARK_SPACE_DUPLEX",
                    "frequency_hz": 2400000000,
                    "bandwidth_hz": 20000000,
                    "antenna_id": "ANT-DARK-01",
                    "telemetry": {
                        "rssi_dbm": round(-68.4 + (random.random() * 2.0 - 1.0), 2),
                        "snr_db": 21.8,
                        "negative_magnetic_field_ut": round(-52.4 * math.sin(t * 0.25), 2)
                    }
                },
                "dark_ep_channels": {
                    "channel_mask": "0x3F",
                    "stimulus_interval_ms": 50,
                    "evoked_potential_amplitude_uv": round(12.5 + random.random() * 2.0, 2),
                    "polarity_inversion_state": "ACTIVE",
                    "evoked_potential_status": "LOCKED"
                },
                "third_world_signal_compartment": {
                    "origin_universe": "NEO-DETACHED-01",
                    "signal_hop_mode": "STEALTH_PARALLEL_MIRROR",
                    "attenuation_db": -112.4
                },
                "microwave_maser_band": {
                    "frequency_ghz": 24.125,
                    "maser_emission_mw": 450.2,
                    "coherence_factor": 0.987
                },
                "satellite_bot_capsule": {
                    "capsule_id": "D3M13N-CAPSULE-SAT-01",
                    "orbit_mode": "GEO_SYNCHRONOUS_MIRROR",
                    "disaster_recovery_status": "ARMED_AUTO_RESTORE",
                    "avatar_encapsulation": "ACTIVE"
                },
                "v2_kinetic_vector": {
                    "velocity_mps": [0.012, -0.005, 0.002],
                    "acceleration_mps2": [0.0001, -0.0002, 0.0000],
                    "kinetic_energy_j": 0.0042,
                    "trajectory_status": "STABLE"
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
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer(("127.0.0.1", 8080), DarkEPKineticHandler)
    print("[DARK EP KINETIC NODE ACTIVE] Telemetry stream running on port 8080")
    server.serve_forever()
