import urllib.request
import json
import time

url = "http://localhost:8080/"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'D3M13N-CAPSULECRAFT-Telemetry-Agent'})
    with urllib.request.urlopen(req, timeout=5) as response:
        status_code = response.status
        headers = dict(response.headers)
        content_length = headers.get('Content-Length', 'Unknown')
        content_type = headers.get('Content-Type', 'Unknown')

    diagnostic_payload = {
        "timestamp": int(time.time()),
        "target_node": url,
        "dba_name": "D3M13N CAPSULECRAFT",
        "jurisdiction": "Harris County / Southern District, Houston Division",
        "http_status": status_code,
        "content_type": content_type,
        "content_length": content_length,
        "connection_state": "VERIFIED_ACTIVE"
    }

    print(json.dumps(diagnostic_payload, indent=2))
    print("\n[+] Matrix node interrogation successful. Endpoint responding with HTTP 200 under active telemetry lock.")

except Exception as e:
    error_payload = {
        "timestamp": int(time.time()),
        "target_node": url,
        "dba_name": "D3M13N CAPSULECRAFT",
        "connection_state": "FAILED",
        "error": str(e)
    }
    print(json.dumps(error_payload, indent=2))
    print("\n[-] Error: Unable to reach active matrix node endpoint.")
