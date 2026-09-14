import socket
import json

def listen_for_mesh_pulse():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', 8080))
    
    print("[+] Matrix listener active on 127.0.0.1:8080. Awaiting telemetry/pulse frames...")
    
    try:
        while True:
            data, addr = sock.recvfrom(4096)
            payload = json.loads(data.decode('utf-8'))
            print(f"\n[+] Received verified mesh packet from {addr}:")
            print(json.dumps(payload, indent=2))
            break  # Exit after capturing one complete frame for verification
    except Exception as e:
        print(f"[-] Listener error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    listen_for_mesh_pulse()
