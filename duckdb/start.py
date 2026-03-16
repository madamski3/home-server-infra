import os
import signal
import duckdb

DB_PATH   = os.environ.get("DUCKDB_FILE", "/data/analytics.duckdb")
HTTP_HOST = "0.0.0.0"
HTTP_PORT = int(os.environ.get("DUCKDB_HTTP_PORT", "9999"))
API_KEY   = os.environ.get("DUCKDB_API_KEY", "")  # empty = no auth (relies on Tailscale for access control)

print(f"Connecting to DuckDB at {DB_PATH}")
con = duckdb.connect(DB_PATH)

# Persist extension binary into the data volume so re-downloads are avoided
# on container rebuilds
con.execute("SET extension_directory='/data/extensions'")

print("Installing httpserver extension...")
con.execute("INSTALL httpserver FROM community")
con.execute("LOAD httpserver")

print(f"Starting HTTP server on {HTTP_HOST}:{HTTP_PORT}")
con.execute(f"SELECT httpserve_start('{HTTP_HOST}', {HTTP_PORT}, '{API_KEY}')")
print("DuckDB HTTP server running.")


def handle_shutdown(signum, frame):
    print("Shutting down...")
    try:
        con.execute("SELECT httpserve_stop()")
    except Exception:
        pass
    con.close()
    raise SystemExit(0)


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)

signal.pause()  # Block until signal; consumes no CPU
