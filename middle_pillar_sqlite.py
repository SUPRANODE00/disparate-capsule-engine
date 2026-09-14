#!/usr/bin/env python3
import json
import sqlite3
import time

DB_NAME = "matrix_production_telemetry.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS telemetry_frames (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resource_id TEXT NOT NULL,
        status TEXT NOT NULL,
        pos_east_m REAL,
        pos_north_m REAL,
        pos_up_m REAL,
        frequency_hz INTEGER,
        right_pillar_bt_nt REAL,
        left_pillar_bz_nt REAL,
        equilibrium_factor REAL,
        raw_payload TEXT,
        timestamp TEXT NOT NULL
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON telemetry_frames (timestamp);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_resource_id ON telemetry_frames (resource_id);")
    conn.commit()
    conn.close()

def generate_sample_frame(timestamp_str):
    return {
        "resource_id": "NODE-HOUSTON-GRID-01",
        "position_enu_m": [6.0, 4.0, 2.0],
        "status": "OPERATIONAL",
        "rf": {
            "mode": "TX_RX",
            "frequency_hz": 13179000,
            "bandwidth_hz": 1000000,
            "telemetry": {
                "rssi_dbm": -67,
                "snr_db": 18
            }
        },
        "magnetic": {
            "right_pillar_bt_nt": 48.2,
            "left_pillar_bz_nt": 49.5,
            "equilibrium_factor": 0.9719
        },
        "timestamp": timestamp_str
    }

def persist_frame(frame):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO telemetry_frames (
        resource_id, status, pos_east_m, pos_north_m, pos_up_m,
        frequency_hz, right_pillar_bt_nt, left_pillar_bz_nt,
        equilibrium_factor, raw_payload, timestamp
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        frame["resource_id"],
        frame["status"],
        frame["position_enu_m"][0],
        frame["position_enu_m"][1],
        frame["position_enu_m"][2],
        frame["rf"]["frequency_hz"],
        frame["magnetic"]["right_pillar_bt_nt"],
        frame["magnetic"]["left_pillar_bz_nt"],
        frame["magnetic"]["equilibrium_factor"],
        json.dumps(frame),
        frame["timestamp"]
    ))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"=== EXECUTION PIPELINE ACTIVE | DB: {DB_NAME} ===")
    base_time = int(time.time())
    for i in range(3):
        ts = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(base_time + i))
        frame = generate_sample_frame(ts)
        persist_frame(frame)
        print(f"[{i+1}/3] Persisted Frame at {frame['timestamp']} | Eq: {frame['magnetic']['equilibrium_factor']} | Freq: {frame['rf']['frequency_hz']} Hz")
