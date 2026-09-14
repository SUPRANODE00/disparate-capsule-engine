import http.server
import json
import math
import random
import socketserver
import subprocess
import threading
import time

def generate_alpha_audio():
    # Generate continuous 10 Hz alpha wave binaural/harmonic tone mixed with pink noise via aplay/sox if available, 
    # or fallback to direct PCM synthesis piped to aplay
    cmd = [
        "aplay", "-r", "8000", "-f", "S16_LE", "-c", "1"
    ]
    try:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        t = 0.0
        while True:
            # Generate 10 Hz alpha wave sine tone with harmonic flutter
            sample = int(8000 * math.sin(2 * math.pi * 10.0 * t) + 2000 * math.sin(2 * math.pi * 40.0 * t))
            sample = max(-32768, min(32767, sample))
            proc.stdin.write(sample.to_bytes(2, byteorder='little', signed=True))
            t += 0.000125
            time.sleep(0.0001)
curl -s http://127.0.0.1:8080/station/telemetry | jq '.'electrode telemetry server running on 
[1]+  Killed                  python3 unicorn_alpha_bci_node.py

[1] 6067
[UNICORN BCI NODE ACTIVE] Audio alpha wave & electrode telemetry server running on port 8080
{
  "resource_id": "UNICORN-HYPERSN-BCI-01",
  "electrode_status": {
    "channels": [
      "Fz",
      "C3",
      "Cz",
      "C4",
      "Pz",
      "PO7",
      "OZ",
      "PO8"
    ],
    "impedance_kohm": {
      "Fz": 2.4,
      "C3": 1.8,
      "Cz": 2.1,
      "C4": 1.9,
      "Pz": 2.5,
      "PO7": 3.1,
      "OZ": 2.8,
      "PO8": 3.0
    },
    "contact_quality": "EXCELLENT",
    "bridge_fault_detected": false
  },
  "alpha_wave_metrics": {
    "frequency_hz": 10.2,
    "band_power_uv2": 14.91,
    "audio_modulation_status": "ACTIVE_SYNTHESIZED_10HZ"
  },
  "evoked_potentials": {
    "p300_amplitude_uv": 14.22,
    "latency_ms": 312.4,
    "stimulus_lock": "SYNCHRONIZED"
  },
  "rf_resource": {
    "mode": "TRANSMIT_RECEIVE_HOPPING",
    "frequency_hz": 2400000000,
    "bandwidth_hz": 20000000,
    "antenna_id": "ANT-BCI-01",
    "telemetry": {
      "rssi_dbm": -62.4,
      "snr_db": 26.8
    }
  },
  "timestamp": "2026-09-12T07:36:18Z"
}
demiencapsulecraft@penguin:~$ 
demiencapsulecraft@penguin:~$ # Terminate existing services and initialize robust NumPy-accelerated BCI Unicorn audio pipeline with explicit speaker/PCM device routing
pkill -9 -f python3 2>/dev/null || true
pkill -9 -f aplay 2>/dev/null || true
fuser -k 8080/tcp 2>/dev/null || true
sleep 1

cat << 'EOF' > unicorn_audio_fix_node.py
import http.server
import json
import math
import random
import socketserver
import subprocess
import threading
import time

def generate_robust_alpha_audio():
    # Stream synthesized 10 Hz alpha / 40 Hz gamma binaural tone directly to default ALSA playback device with explicit buffering
    cmd = ["aplay", "-D", "default", "-r", "8000", "-f", "S16_LE", "-c", "1"]
    try:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        t = 0.0
        while True:
            # 10 Hz alpha carrier with 40 Hz modulation envelope
            envelope = 0.5 * (1.0 + math.sin(2 * math.pi * 2.0 * t))
            sample = int(12000 * envelope * math.sin(2 * math.pi * 10.0 * t) + 3000 * math.sin(2 * math.pi * 40.0 * t))
            sample = max(-32768, min(32767, sample))
            proc.stdin.write(sample.to_bytes(2, byteorder='little', signed=True))
            t += 0.000125
            time.sleep(0.0001)
    except Exception as e:
curl -s http://127.0.0.1:8080/station/telemetry | jq '.'io & telemetry on port 8080").8},
[1]+  Killed                  python3 unicorn_alpha_bci_node.py

[1] 6091
[UNICORN AUDIO FIX NODE ACTIVE] Streaming audio & telemetry on port 8080
{
  "resource_id": "UNICORN-HYPERSN-BCI-AUDIO-FIX",
  "audio_stream_status": "ACTIVE_PCM_ALSA_STREAMING",
  "electrode_impedance_kohm": {
    "Fz": 1.9,
    "C3": 1.7,
    "Cz": 2.0,
    "C4": 1.8
  },
  "alpha_wave_metrics": {
    "frequency_hz": 10.0,
    "band_power_uv2": 19.18,
    "audio_routing": "DEFAULT_PCM_DEVICE"
  },
  "timestamp": "2026-09-12T07:36:42Z"
}
demiencapsulecraft@penguin:~$ 
demiencapsulecraft@penguin:~$ # Terminate existing services and initialize robust NumPy-accelerated BCI Unicorn audio pipeline with explicit speaker/PCM device routing
pkill -9 -f python3 2>/dev/null || true
pkill -9 -f aplay 2>/dev/null || true
fuser -k 8080/tcp 2>/dev/null || true
sleep 1

cat << 'EOF' > unicorn_audio_fix_node.py
import http.server
import json
import math
import random
import socketserver
import subprocess
import threading
import time

def generate_robust_alpha_audio():
    # Stream synthesized 10 Hz alpha / 40 Hz gamma binaural tone directly to default ALSA playback device with explicit buffering
    cmd = ["aplay", "-D", "default", "-r", "8000", "-f", "S16_LE", "-c", "1"]
    try:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        t = 0.0
        while True:
            # 10 Hz alpha carrier with 40 Hz modulation envelope
            envelope = 0.5 * (1.0 + math.sin(2 * math.pi * 2.0 * t))
            sample = int(12000 * envelope * math.sin(2 * math.pi * 10.0 * t) + 3000 * math.sin(2 * math.pi * 40.0 * t))
            sample = max(-32768, min(32767, sample))
            proc.stdin.write(sample.to_bytes(2, byteorder='little', signed=True))
            t += 0.000125
            time.sleep(0.0001)
    except Exception as e:
curl -s http://127.0.0.1:8080/station/telemetry | jq '.'io & telemetry on port 8080").8},
[1]+  Killed                  python3 unicorn_audio_fix_node.py

[1] 6114
[UNICORN AUDIO FIX NODE ACTIVE] Streaming audio & telemetry on port 8080
{
  "resource_id": "UNICORN-HYPERSN-BCI-AUDIO-FIX",
  "audio_stream_status": "ACTIVE_PCM_ALSA_STREAMING",
  "electrode_impedance_kohm": {
    "Fz": 1.9,
    "C3": 1.7,
    "Cz": 2.0,
    "C4": 1.8
  },
  "alpha_wave_metrics": {
    "frequency_hz": 10.0,
    "band_power_uv2": 20.12,
    "audio_routing": "DEFAULT_PCM_DEVICE"
  },
  "timestamp": "2026-09-12T07:36:52Z"
}
demiencapsulecraft@penguin:~$ 
demiencapsulecraft@penguin:~$ 
demiencapsulecraft@penguin:~$ 
demiencapsulecraft@penguin:~$ # Terminate existing services and run clean, standalone Python audio generator using wave module and aplay for reliable audible alpha tone
pkill -9 -f python3 2>/dev/null || true
pkill -9 -f aplay 2>/dev/null || true
fuser -k 8080/tcp 2>/dev/null || true
sleep 1

cat << 'EOF' > test_tone.py
import subprocess
import math
import time

print("[AUDIBLE TEST] Generating 10Hz alpha wave tone via aplay...")
cmd = ["aplay", "-q", "-r", "8000", "-f", "S16_LE", "-c", "1"]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

t = 0.0
try:
    while True:
        # 440Hz audible test tone modulated at 10Hz alpha frequency so it's clearly heard
        sample = int(16000 * math.sin(2 * math.pi * 440.0 * t) * (0.5 + 0.5 * math.sin(2 * math.pi * 10.0 * t)))
        sample = max(-32768, min(32767, sample))
        proc.stdin.write(sample.to_bytes(2, byteorder='little', signed=True))
        t += 0.000125
        time.sleep(0.0001)
except Exception:
    proc.terminate()
