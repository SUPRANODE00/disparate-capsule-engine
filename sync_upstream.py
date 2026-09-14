import sqlite3
import urllib.request
import json

def dispatch_pending_telemetry():
    conn = sqlite3.connect("inventory_mesh.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, timestamp, resource_id, gateway, payload FROM node_telemetry ORDER BY id DESC LIMIT 1;")
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        print("[!] No records found to dispatch.")
        return

    record_id, ts, res_id, endpoint, payload_str = row
    payload = json.loads(payload_str)
    
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            print(f"[+] Dispatched payload ID {record_id} to {endpoint} -> Status {response.status}")
    except Exception as e:
        print(f"[!] Gateway outbound dispatch failed (logged locally): {e}")

if __name__ == "__main__":
    dispatch_pending_telemetry()
