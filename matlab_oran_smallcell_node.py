import http.server
import json
import math
import random
import socketserver
import time

class MatlabOranSmallCellHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        clean_path = self.path.rstrip('/')
        
        if clean_path == "/station/telemetry":
            t = time.time()
            # Spherical coordinate tracking for O-RAN Small Cell / UAV Mesh Node
            r = 12.8 + math.sin(t * 0.15) * 0.4
            azimuth_rad = (t * 0.3) % (2 * math.pi)
            elevation_rad = 0.7854 # 45 degrees
            
            x_m = r * math.cos(elevation_rad) * math.sin(azimuth_rad)
            y_m = r * math.cos(elevation_rad) * math.cos(azimuth_rad)
            z_m = r * math.sin(elevation_rad)

            payload = {
                "resource_id": "D3M13N-ORAN-SMALLCELL-01",
                "node_role": "ANTENNA_NODE_PERSON_MATRIX",
                "coordinate_system": "SPHERICAL_TO_ENU",
                "position_spherical": {
                    "radius_m": round(r, 4),
                    "azimuth_deg": round(math.degrees(azimuth_rad), 2),
                    "elevation_deg": round(math.degrees(elevation_rad), 2)
                },
                "position_enu_m": [round(x_m, 2), round(y_m, 2), round(z_m, 2)],
                "oran_architecture": {
                    "functional_split": "SPLIT_7_2_X",
                    "components": ["O-RU", "O-DU", "O-CU"],
                    "multi_rat_active": ["5G_NR", "LTE", "MESH_IOT", "WIFI_6"],
                    "synchronization": "IEEE_1588_LOCKED"
                },
                "semiconductor_packaging": {
                    "dielectric_interface": "ULK_LOW_K",
                    "trap_density_cm2": "4.2e12",
                    "packaging_type": "SIP_SAP_HDI"
                },
                "rf_resource": {
                    "mode": "TRANSMIT_RECEIVE_HOPPING",
                    "frequency_hz": 2400000000,
                    "bandwidth_hz": 20000000,
                    "antenna_id": "ANT-ORAN-01",
                    "telemetry": {
                        "rssi_dbm": round(-65.4 + (random.random() * 2.0 - 1.0), 2),
                        "snr_db": 25.1,
                        "doppler_shift_hz": round(142.2 * math.sin(t * 0.5), 2)
                    }
                },
                "dark_ep_channels": {
                    "channel_mask": "0x3F",
                    "evoked_potential_amplitude_uv": round(14.2 + random.random() * 1.5, 2),
                    "polarity_inversion_state": "ACTIVE"
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
    server = socketserver.TCPServer(("127.0.0.1", 8080), MatlabOranSmallCellHandler)
    print("[MATLAB O-RAN SMALL CELL NODE ACTIVE] Telemetry engine running on port 8080")
    server.serve_forever()
