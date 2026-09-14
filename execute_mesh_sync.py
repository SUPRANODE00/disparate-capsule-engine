import os
import json
import zipfile

target_world = "warlock_avatar_grid.mcworld"
workspace = "temp_bedrockmap_workspace"
os.makedirs(workspace, exist_ok=True)

# 1. Compile final mesh coordinate node package
mesh_sync_payload = {
    "node_grid": "ACTIVE",
    "spatial_origin": [0.0, 64.0, 0.0],
    "telemetry_link": "STABLE",
    "rf_nodes": [
        {"resource_id": "RF-NODE-001", "position_enu_m": [3.2, -4.8, 1.7], "rf": {"mode": "RX", "frequency_hz": 2400000000, "bandwidth_hz": 1000000, "antenna_id": "ANT-01", "telemetry": {"rssi_dbm": -61, "snr_db": 18}}},
        {"resource_id": "RF-NODE-002", "position_enu_m": [6.0, 4.0, 2.0], "rf": {"mode": "TX", "frequency_hz": 2412000000, "bandwidth_hz": 2000000, "antenna_id": "ANT-02", "telemetry": {"rssi_dbm": -67, "snr_db": 14}}}
    ]
}

payload_filename = "mesh_sync_status.json"
payload_path = os.path.join(workspace, payload_filename)

with open(payload_path, "w") as f:
    json.dump(mesh_sync_payload, f, indent=2)

print(f"[+] Mesh sync payload compiled: {payload_path}")

# 2. Inject into archive under metadata/
if os.path.exists(target_world):
    with zipfile.ZipFile(target_world, 'a', zipfile.ZIP_DEFLATED) as mcworld_zip:
        mcworld_zip.write(payload_path, f"metadata/{payload_filename}")
    print(f"[+] Mesh synchronization payload successfully embedded into {target_world}")
else:
    print(f"[-] Target archive {target_world} not found.")
