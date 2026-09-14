#!/usr/bin/env python3

import http.server
import json
import math
import random
import socketserver
import time

HOST = "127.0.0.1"
PORT = 8081

CHANNELS = [
    "Fz", "C3", "Cz", "C4",
    "Pz", "PO7", "OZ", "PO8"
]

BASE_IMPEDANCE = {
    "Fz": 2.4,
    "C3": 1.8,
    "Cz": 2.1,
    "C4": 1.9,
    "Pz": 2.5,
    "PO7": 3.1,
    "OZ": 2.8,
    "PO8": 3.0,
}


def telemetry():
    now = time.time()

    impedance = {
        ch: round(
            BASE_IMPEDANCE[ch] + 0.05 * math.sin(now + i),
            2
        )
        for i, ch in enumerate(CHANNELS)
    }

    alpha_frequency = round(
        10.0 + 0.2 * math.sin(now / 3.0),
        2
    )

    band_power = round(
        18.0 + 3.0 * math.sin(now / 4.0),
        2
    )

    p300_amplitude = round(
        13.5 + 1.0 * math.sin(now / 5.0),
        2
    )

    return {
        "simulation": True,
        "resource_id": "UNICORN-HYPERSN-BCI-SIM-01",

        "electrode_status": {
            "channels": CHANNELS,
            "impedance_kohm": impedance,
            "contact_quality": "SIMULATED_EXCELLENT",
            "bridge_fault_detected": False
        },

        "alpha_wave_metrics": {
            "frequency_hz": alpha_frequency,
            "band_power_uv2": band_power,
            "audio_modulation_status": "SYNTHETIC_10HZ"
        },

        "evoked_potentials": {
            "p300_amplitude_uv": p300_amplitude,
            "latency_ms": 312.4,
            "stimulus_lock": "SIMULATED_SYNCHRONIZED"
        },

        "rf_resource": {
            "simulation": True,
            "mode": "TELEMETRY_ONLY",
            "frequency_hz": 2400000000,
            "bandwidth_hz": 20000000,
            "antenna_id": "SIM-ANT-BCI-01",

            "telemetry": {
                "rssi_dbm": -62.4,
                "snr_db": 26.8
            }
        },

        "timestamp": time.strftime(
            "%Y-%m-%dT%H:%M:%SZ",
            time.gmtime()
        )
    }


class Handler(http.server.BaseHTTPRequestHandler):

    def send_json(self, payload, status=200):
        body = json.dumps(
            payload,
            indent=2
        ).encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json"
        )
        self.send_header(
            "Content-Length",
            str(len(body))
        )
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):

        if self.path in (
            "/",
            "/health",
            "/station/telemetry",
            "/telemetry"
        ):
            self.send_json(telemetry())
            return

        self.send_json({
            "error": "not_found",
            "path": self.path
        }, 404)

    def log_message(self, fmt, *args):
        print(
            "[BCI-SIM]",
            fmt % args,
            flush=True
        )


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


if __name__ == "__main__":

    with Server((HOST, PORT), Handler) as server:

        print(
            "[UNICORN BCI SIM ACTIVE]",
            f"http://{HOST}:{PORT}",
            flush=True
        )

        print(
            "[NOTICE] Synthetic telemetry only; "
            "no physical EEG acquisition or RF transmission.",
            flush=True
        )

        server.serve_forever()
