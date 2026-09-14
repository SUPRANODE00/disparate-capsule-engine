#!/usr/bin/env python3

import http.server
import json
import os
import socket
import socketserver
import time
from typing import Any


HOST = os.environ.get("MATRIX_BIND_HOST", "127.0.0.1")
PORT = int(os.environ.get("MATRIX_BIND_PORT", "8080"))

VALID_DIAL_CODE = "*#*#7777*#*#"
RADIUS_M = 50.0
NODES_ACTIVE = 12


def utc_timestamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def json_response(
    handler: http.server.BaseHTTPRequestHandler,
    payload: dict[str, Any],
    status: int = 200,
) -> None:
    encoded = json.dumps(payload, indent=2).encode("utf-8")

    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(encoded)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(encoded)


class MatrixRadiusHandler(http.server.BaseHTTPRequestHandler):

    server_version = "MatrixRadiusIngress/1.0"

    def do_GET(self) -> None:
        if self.path in ("/", "/health", "/healthz"):
            json_response(
                self,
                {
                    "service": "matrix-radius-ingress",
                    "status": "ACTIVE",
                    "bind": f"{HOST}:{PORT}",
                    "radius_m": RADIUS_M,
                    "nodes_active": NODES_ACTIVE,
                    "timestamp": utc_timestamp(),
                },
            )
            return

        json_response(
            self,
            {
                "status": "NOT_FOUND",
                "path": self.path,
                "timestamp": utc_timestamp(),
            },
            404,
        )

    def do_POST(self) -> None:
        if self.path != "/matrix/dial":
            json_response(
                self,
                {
                    "matrix_ingress_ack": "REJECTED_INVALID_PATH",
                    "path": self.path,
                    "timestamp": utc_timestamp(),
                },
                404,
            )
            return

        try:
            content_length = int(
                self.headers.get("Content-Length", "0")
            )
        except ValueError:
            content_length = 0

        # Protect the daemon from unexpectedly large request bodies.
        if content_length > 64 * 1024:
            json_response(
                self,
                {
                    "matrix_ingress_ack": "REJECTED_PAYLOAD_TOO_LARGE",
                    "timestamp": utc_timestamp(),
                },
                413,
            )
            return

        raw_data = self.rfile.read(content_length)

        try:
            req = json.loads(raw_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            json_response(
                self,
                {
                    "matrix_ingress_ack": "REJECTED_INVALID_JSON",
                    "timestamp": utc_timestamp(),
                },
                400,
            )
            return

        if not isinstance(req, dict):
            json_response(
                self,
                {
                    "matrix_ingress_ack": "REJECTED_INVALID_REQUEST",
                    "timestamp": utc_timestamp(),
                },
                400,
            )
            return

        dial_code = req.get("dial_code", "")

        if dial_code == VALID_DIAL_CODE:
            response_payload = {
                "matrix_ingress_ack": "SUCCESS",
                "radius_sweep_status": "ACTIVE_3D_MAPPING_ENROUTE",
                "agent_mesh_status": "STREAMING_INTO_LOCAL_RADIUS",
                "transport": {
                    "protocol": "HTTP",
                    "bind_host": HOST,
                    "bind_port": PORT,
                    "loopback_only": HOST in ("127.0.0.1", "localhost"),
                },
                "geo_pose": {
                    "coordinate_frame": "LOCAL_CARTESIAN",
                    "origin_xyz": [0.0, 0.0, 0.0],
                    "radius_m": RADIUS_M,
                    "nodes_active": NODES_ACTIVE,
                },
                "timestamp": utc_timestamp(),
            }

            json_response(self, response_payload, 200)

        else:
            json_response(
                self,
                {
                    "matrix_ingress_ack": "REJECTED_UNKNOWN_DIAL_CODE",
                    "dial_code_received": dial_code,
                    "timestamp": utc_timestamp(),
                },
                400,
            )

    def log_message(self, fmt: str, *args: Any) -> None:
        timestamp = utc_timestamp()
        print(f"[{timestamp}] {self.address_string()} {fmt % args}")


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


def verify_bind(host: str, port: int) -> None:
    with socket.create_connection((host, port), timeout=2):
        pass


if __name__ == "__main__":
    print("=" * 64)
    print(" MATRIX RADIUS INGRESS AGENT")
    print("=" * 64)
    print(f" Bind       : {HOST}:{PORT}")
    print(f" Radius     : {RADIUS_M} m")
    print(f" Nodes      : {NODES_ACTIVE}")
    print(f" Endpoint   : POST /matrix/dial")
    print(f" Health     : GET  /health")
    print("=" * 64)

    try:
        with ReusableTCPServer((HOST, PORT), MatrixRadiusHandler) as server:

            # Confirm the kernel accepted the bind before entering
            # the blocking foreground service loop.
            verify_bind(HOST, PORT)

            print(
                f"[MATRIX RADIUS INGRESS AGENT ACTIVE] "
                f"Listening on {HOST}:{PORT}"
            )
            print("[BIND VERIFIED]")
            print("[FOREGROUND DAEMON READY]")

            server.serve_forever()

    except OSError as exc:
        print(f"[FATAL] Unable to bind {HOST}:{PORT}: {exc}")
        raise SystemExit(1)

    except KeyboardInterrupt:
        print("\n[MATRIX RADIUS INGRESS] Shutdown requested.")
