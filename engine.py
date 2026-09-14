import json
import os
import re
from datetime import datetime, timezone

def validate_allocation_payload(payload):
    """
    Validates an InitiateAllocationPayload dictionary against structural rules.
    """
    print("\n[+] Validating InitiateAllocationPayload...")
    required_fields = ["entity_id", "timestamp_utc", "jurisdiction", "administrative_status"]
    
    # Check required fields
    missing = [f for f in required_fields if f not in payload]
    if missing:
        print(f"[-] Validation Failed: Missing required fields {missing}")
        return False

    # Check Regex pattern for entity_id
    pattern = r"^REG-\d{4}-[A-Z]{2,4}-[a-f0-9]{8}$"
    if not re.match(pattern, payload["entity_id"]):
        print(f"[-] Validation Failed: entity_id '{payload['entity_id']}' invalid regex pattern.")
        return False

    # Check Enum for administrative_status
    valid_statuses = ["PENDING", "ACTIVE", "SUSPENDED", "DETACHED"]
    if payload["administrative_status"] not in valid_statuses:
        print(f"[-] Validation Failed: administrative_status must be one of {valid_statuses}")
        return False

    print(f"[✓] Payload Validated Successfully for Entity: {payload['entity_id']}")
    return True

def display_rf_telemetry(data):
    """
    Parses and displays RF Resource telemetry structure.
    """
    res_id = data.get("resource_id", "N/A")
    pos = data.get("position_enu_m", [0.0, 0.0, 0.0])
    rf = data.get("rf", {})
    telem = rf.get("telemetry", {})

    print("\n" + "="*50)
    print(f" TELEMETRY RESOURCE READOUT: {res_id}")
    print("="*50)
    print(f" ENU Position Vector : [East: {pos[0]}m, North: {pos[1]}m, Up: {pos[2]}m]")
    print(f" RF Mode / Antenna   : {rf.get('mode', 'N/A')} | Antenna: {rf.get('antenna_id', 'N/A')}")
    print(f" Operating Freq      : {rf.get('frequency_hz', 0) / 1e6:.2f} MHz")
    print(f" Bandwidth           : {rf.get('bandwidth_hz', 0) / 1e3:.1f} kHz")
    print(f" Signal Metrics      : RSSI {telem.get('rssi_dbm', 'N/A')} dBm | SNR {telem.get('snr_db', 'N/A')} dB")
    print("="*50 + "\n")

if __name__ == "__main__":
    sample_allocation = {
        "entity_id": "REG-2026-TX-a1b2c3d4",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "jurisdiction": "US-TX-HOU",
        "administrative_status": "ACTIVE",
        "origin_affinity": "TST_ORIGIN"
    }
    
    validate_allocation_payload(sample_allocation)

    sample_rf = {
        "resource_id": "RF-NODE-TRIAGE-01",
        "position_enu_m": [6.0, 4.0, 2.0],
        "rf": {
            "mode": "RX",
            "frequency_hz": 2400000000,
            "bandwidth_hz": 1000000,
            "antenna_id": "ANT-TRIAGE",
            "telemetry": {
                "rssi_dbm": -67,
                "snr_db": 18
            }
        }
    }
    display_rf_telemetry(sample_rf)
