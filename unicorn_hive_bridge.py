#!/usr/bin/env python3

import json
import os
import ssl
import sys
import time
import urllib.request
import urllib.error

import paho.mqtt.client as mqtt


HTTP_TELEMETRY = os.environ.get(
    "HTTP_TELEMETRY",
    "http://127.0.0.1:8081/station/telemetry"
)

MQTT_HOST = os.environ.get("HIVE_MQTT_HOST")
MQTT_PORT = int(
    os.environ.get("HIVE_MQTT_PORT", "8883")
)

MQTT_USER = os.environ.get("HIVE_MQTT_USER")
MQTT_PASS = os.environ.get("HIVE_MQTT_PASS")

MQTT_TOPIC = os.environ.get(
    "HIVE_MQTT_TOPIC",
    "SL1TH3R/UNICORN/BCI-SIM/telemetry"
)


def require_environment():
    missing = []

    for name, value in {
        "HIVE_MQTT_HOST": MQTT_HOST,
        "HIVE_MQTT_USER": MQTT_USER,
        "HIVE_MQTT_PASS": MQTT_PASS,
    }.items():
        if not value:
            missing.append(name)

    if missing:
        print(
            "[FATAL] Missing environment variables:",
            ", ".join(missing),
            flush=True
        )
        sys.exit(1)


def fetch_telemetry():
    try:
        with urllib.request.urlopen(
            HTTP_TELEMETRY,
            timeout=5
        ) as response:

            raw = response.read()
            return json.loads(
                raw.decode("utf-8")
            )

    except urllib.error.URLError as exc:
        print(
            f"[TELEMETRY ERROR] {exc}",
            flush=True
        )
        return None

    except Exception as exc:
        print(
            f"[TELEMETRY ERROR] {exc}",
            flush=True
        )
        return None


def on_connect(
    client,
    userdata,
    flags,
    reason_code,
    properties=None
):
    print(
        f"[HIVE CONNECT] reason={reason_code}",
        flush=True
    )


def on_disconnect(
    client,
    userdata,
    disconnect_flags,
    reason_code,
    properties=None
):
    print(
        f"[HIVE DISCONNECT] reason={reason_code}",
        flush=True
    )


def main():

    require_environment()

    print(
        "[HIVE BRIDGE INITIALIZING]",
        flush=True
    )

    print(
        f"[LOCAL SOURCE] {HTTP_TELEMETRY}",
        flush=True
    )

    print(
        f"[MQTT TARGET] {MQTT_HOST}:{MQTT_PORT}",
        flush=True
    )

    print(
        f"[MQTT TOPIC] {MQTT_TOPIC}",
        flush=True
    )

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="UNICORN-HIVE-BCI-SIM-01"
    )

    client.username_pw_set(
        MQTT_USER,
        MQTT_PASS
    )

    client.tls_set(
        cert_reqs=ssl.CERT_REQUIRED
    )

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    try:

        client.connect(
            MQTT_HOST,
            MQTT_PORT,
            keepalive=60
        )

        client.loop_start()

        while True:

            payload = fetch_telemetry()

            if payload is not None:

                payload["simulation"] = True

                payload["transport"] = {
                    "protocol": "MQTT",
                    "topic": MQTT_TOPIC
                }

                message = json.dumps(
                    payload,
                    separators=(",", ":")
                )

                info = client.publish(
                    MQTT_TOPIC,
                    message,
                    qos=1,
                    retain=False
                )

                info.wait_for_publish()

                print(
                    "[HIVE PUBLISH]",
                    f"resource={payload.get('resource_id')}",
                    f"bytes={len(message)}",
                    flush=True
                )

            time.sleep(1)

    except KeyboardInterrupt:

        print(
            "\n[HIVE BRIDGE] Shutdown requested.",
            flush=True
        )

    except Exception as exc:

        print(
            f"[FATAL] {exc}",
            flush=True
        )

        raise

    finally:

        try:
            client.loop_stop()
            client.disconnect()
        except Exception:
            pass


if __name__ == "__main__":
    main()
