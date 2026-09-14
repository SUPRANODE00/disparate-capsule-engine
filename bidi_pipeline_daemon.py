#!/usr/bin/env python3
import json
import os
import sqlite3
import time
from bidi_core import BidiStreamParser, LRI, RLI, PDI

DB_NAME = os.getenv("DB_NAME", "matrix_production_telemetry.db")

def init_bidi_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bidi_pipeline_frames (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resource_id TEXT NOT NULL,
        bidi_payload TEXT NOT NULL,
        polarity_ratio REAL NOT NULL,
        is_balanced INTEGER NOT NULL,
        pos_east_m REAL,
        pos_north_m REAL,
        pos_up_m REAL,
        timestamp TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

def generate_bidi_frame():
    ts = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    node_id = os.getenv("RESOURCE_ID", "BIDI-NODE-HOUSTON-01")
    
    backend_data = json.dumps({
        "mode": "ACTIVE_TX",
        "freq_hz": int(os.getenv("RF_FREQUENCY_HZ", 13179000)),
        "rssi_dbm": -67
    })
    
    frontend_data = json.dumps({
        "viewport": "3D_RADAR_WEBGL",
        "render_fps": 60,
        "theme": "BLACKLIGHT"
    })

    bidi_backend_stream = BidiStreamParser.encapsulate_backend(backend_data)
    bidi_frontend_stream = BidiStreamParser.encapsulate_frontend(frontend_data)

    fused_bidi_payload = f"\u2068{bidi_backend_stream}<==EQUILIBRIUM_BUS==>{bidi_frontend_stream}{PDI}"

    metrics = BidiStreamParser.parse_stream(fused_bidi_payload)

    return {
        "resource_id": node_id,
        "bidi_payload": fused_bidi_payload,
        "polarity_ratio": metrics["polarity_ratio"],
        "is_balanced": 1 if metrics["balanced"] else 0,
        "position_enu": [
            float(os.getenv("POS_EAST_M", 6.0)),
            float(os.getenv("POS_NORTH_M", 4.0)),
            float(os.getenv("POS_UP_M", 2.0))
        ],
        "timestamp": ts
    }

def persist_bidi_frame(frame):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO bidi_pipeline_frames (
        resource_id, bidi_payload, polarity_ratio, is_balanced,
        pos_east_m, pos_north_m, pos_up_m, timestamp
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        frame["resource_id"],
        frame["bidi_payload"],
        frame["polarity_ratio"],
        frame["is_balanced"],
        frame["position_enu"][0],
        frame["position_enu"][1],
        frame["position_enu"][2],
        frame["timestamp"]
    ))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_bidi_db()
    frame = generate_bidi_frame()
    persist_bidi_frame(frame)
    print(f"[+] Persisted Bidi-Encapsulated Frame for {frame['resource_id']}")
    print(f"    Payload Stream: {repr(frame['bidi_payload'])}")
    print(f"    Polarity Balanced: {bool(frame['is_balanced'])}")
