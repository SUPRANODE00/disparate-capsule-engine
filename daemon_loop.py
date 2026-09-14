import time
import repl_engine

def start_sync_loop(interval_sec=10):
    print(f"[*] Node telemetry daemon active. Syncing every {interval_sec} seconds...")
    while True:
        try:
            cfg = repl_engine.load_config()
            repl_engine.persist_to_db(cfg)
            time.sleep(interval_sec)
        except KeyboardInterrupt:
            print("\n[-] Sync daemon stopped.")
            break
        except Exception as e:
            print(f"[!] Sync error: {e}")
            time.sleep(interval_sec)

if __name__ == "__main__":
    start_sync_loop()
