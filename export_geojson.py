#!/usr/bin/env python3
import json
import sqlite3

DB_NAME = "matrix_production_telemetry.db"
OUTPUT_FILE = "telemetry_stream.geojson"

def export_to_geojson():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            id, resource_id, status, 
            pos_east_m, pos_north_m, pos_up_m, 
            frequency_hz, right_pillar_bt_nt, left_pillar_bz_nt, 
            equilibrium_factor, timestamp 
        FROM telemetry_frames
        ORDER BY id ASC;
    """)
    rows = cursor.fetchall()
    conn.close()

    features = []
    for row in rows:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row[3], row[4], row[5]]
            },
            "properties": {
                "id": row[0],
                "resource_id": row[1],
                "status": row[2],
                "frequency_hz": row[6],
                "right_pillar_bt_nt": row[7],
                "left_pillar_bz_nt": row[8],
                "equilibrium_factor": row[9],
                "timestamp": row[10]
            }
        }
        features.append(feature)

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(geojson_data, f, indent=4)

    print(f"SUCCESS: Exported {len(features)} frames to {OUTPUT_FILE}")

if __name__ == "__main__":
    export_to_geojson()
