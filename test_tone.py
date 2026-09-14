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
