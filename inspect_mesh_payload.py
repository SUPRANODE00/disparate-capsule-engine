import zipfile
import json

target_world = "warlock_avatar_grid.mcworld"
with zipfile.ZipFile(target_world, 'r') as z:
    print("[*] Inspecting metadata/mesh_sync_status.json contents:")
    payload_data = z.read("metadata/mesh_sync_status.json").decode("utf-8")
    print(json.dumps(json.loads(payload_data), indent=2))
