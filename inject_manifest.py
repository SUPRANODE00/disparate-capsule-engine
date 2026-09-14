import os
import json
import zipfile

workspace = "temp_bedrockmap_workspace"
os.makedirs(workspace, exist_ok=True)

crypto_manifest = {
    "crypto_endpoints": {
        "SOL": "9dE8CHJ778WzdRrQkXgPdB3mc1nahTMxq1oJcFLD1RMx",
        "ETH": "0x027124Aa627Ba33F00c133d19437FC9d9C236052",
        "BTC": "bc1ptwuh2nxacv8j77qthlnnlgquu7ycydjf9gupwlq7dghg24padptqmvvpag"
    },
    "entity_metadata": {
        "dba_name": "D3M13N CAPSULECRAFT",
        "ein": "42-431948",
        "principal": "Erik Ivan Rivera",
        "jurisdiction": "Harris County District Court / Southern District, Houston Division"
    }
}

manifest_filename = "crypto_manifest.json"
manifest_path = os.path.join(workspace, manifest_filename)

with open(manifest_path, "w") as f:
    json.dump(crypto_manifest, f, indent=2)

print(f"[+] Crypto routing manifest generated: {manifest_path}")

target_world = "warlock_avatar_grid.mcworld"
if os.path.exists(target_world):
    with zipfile.ZipFile(target_world, 'a', zipfile.ZIP_DEFLATED) as mcworld_zip:
        mcworld_zip.write(manifest_path, f"metadata/{manifest_filename}")
    print(f"[+] Manifest successfully injected into {target_world} archive under metadata/")
else:
    print(f"[-] Target archive {target_world} not found.")
