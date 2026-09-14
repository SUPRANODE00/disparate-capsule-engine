#!/usr/bin/env bash

# Use local loopback where server.js is currently running
INGEST_URL="http://127.0.0.1:8080/api/v1/telemetry/ingest"
# Uncomment for remote edge routing once Cloudflare/Nginx proxy is live:
# INGEST_URL="https://telemetry.blackcorp.me/api/v1/telemetry/ingest"

NODE_ID="RF-NODE-77034-ALPHA"
MEMBER_ID="DEMIEN-CAPSULECRAFT-01"

echo "[+] Starting RF Telemetry Stream Simulator -> ${INGEST_URL}"

X=0.0
Y=0.0
Z=5.0
ANGLE=0

while true; do
  X=$(awk "BEGIN {print 15.0 * cos($ANGLE)}")
  Y=$(awk "BEGIN {print 15.0 * sin($ANGLE)}")
  Z=$(awk "BEGIN {print 5.0 + 2.0 * sin($ANGLE * 2)}")
  
  RSSI=$(awk "BEGIN {print -65.0 + (rand() * 10 - 5)}")
  SNR=$(awk "BEGIN {print 22.0 + (rand() * 4 - 2)}")
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  PAYLOAD=$(cat <<JSON
{
  "member_id": "${MEMBER_ID}",
  "resource_id": "${NODE_ID}",
  "position_enu_m": [${X}, ${Y}, ${Z}],
  "rf": {
    "mode": "TX",
    "frequency_hz": 2450000000,
    "bandwidth_hz": 20000000,
    "antenna_id": "ANT-OMNI-01",
    "telemetry": {
      "rssi_dbm": ${RSSI},
      "snr_db": ${SNR}
    }
  },
  "timestamp": "${TIMESTAMP}"
}
JSON
  )

  RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${INGEST_URL}" \
    -H "Content-Type: application/json" \
    -d "${PAYLOAD}")

  echo "[${TIMESTAMP}] Target: ${NODE_ID} | ENU: [${X}, ${Y}, ${Z}] | Status: ${RESPONSE}"

  ANGLE=$(awk "BEGIN {print ${ANGLE} + 0.1}")
  sleep 1
done
