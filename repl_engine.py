import tomllib
import sqlite3
import json
from datetime import datetime, timezone

def load_config():
    with open("node_config.toml", "rb") as f:
        return tomllib.load(f)

def persist_to_db(config):
    conn = sqlite3.connect("inventory_mesh.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS node_telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            resource_id TEXT,
            gateway TEXT,
            dispatch_contact TEXT,
            payload JSON
        )
    """)
    now = datetime.now(timezone.utc).isoformat()
    cursor.execute(
        "INSERT INTO node_telemetry (timestamp, resource_id, gateway, dispatch_contact, payload) VALUES (?, ?, ?, ?, ?)",
        (
            now,
            config["node_identity"]["resource_id"],
            config["node_identity"]["gateway_endpoint"],
            config["node_identity"]["dispatch_contact"],
            json.dumps(config)
        )
    )
    conn.commit()
    conn.close()
    print(f"[+] Logged TOML telemetry state to inventory_mesh.db at {now}")

def run_repl():
    config = load_config()
    persist_to_db(config)
    print("\n--- CAPSULE REPL ACTIVE ---")
    print("Commands: 'status', 'rf', 'sync', 'exit'")
    while True:
        try:
            cmd = input("node-repl> ").strip().lower()
            if cmd == "status":
                print(f"Resource ID: {config['node_identity']['resource_id']}")
                print(f"Gateway:     {config['node_identity']['gateway_endpoint']}")
                print(f"Contact:     {config['node_identity']['dispatch_contact']}")
            elif cmd == "rf":
                print(f"Mode: {config['rf_resource']['mode']} | Freq: {config['rf_resource']['frequency_hz']}Hz | RSSI: {config['rf_resource']['rssi_dbm']}dBm")
            elif cmd == "sync":
                persist_to_db(config)
            elif cmd in ("exit", "quit"):
                print("Exiting REPL.")
                break
            else:
                print("Unknown command. Options: status, rf, sync, exit")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting REPL.")
            break

if __name__ == "__main__":
    run_repl()
