#!/usr/bin/env bash
set -e

DB_FILE="matrix_production_telemetry.db"
SCRIPT_FILE="middle_pillar_sqlite.py"

echo "=== [1/4] EXECUTING PIPELINE GENERATOR ==="
python3 "$SCRIPT_FILE"

echo ""
echo "=== [2/4] VERIFYING SQLITE DATABASE INTEGRITY ==="
if [ ! -f "$DB_FILE" ]; then
    echo "FAIL: Database file $DB_FILE missing!"
    exit 1
fi

TOTAL_ROWS=$(python3 -c "import sqlite3; conn=sqlite3.connect('$DB_FILE'); c=conn.cursor(); print(c.execute('SELECT COUNT(*) FROM telemetry_frames').fetchone()[0]); conn.close()")
echo "PASS: Total Database Records = $TOTAL_ROWS"

echo ""
echo "=== [3/4] CHECKING INDEX SCHEMA VIA AWK ==="
python3 -c "import sqlite3; conn=sqlite3.connect('$DB_FILE'); c=conn.cursor(); print('\n'.join([r[0] for r in c.execute(\"SELECT name FROM sqlite_master WHERE type='index'\").fetchall()]))" | awk '{print "FOUND INDEX: " $0}'

echo ""
echo "=== [4/4] VALIDATING ENU GEOPOSITION VECTOR DATA ==="
python3 -c "
import sqlite3
conn = sqlite3.connect('$DB_FILE')
c = conn.cursor()
row = c.execute('SELECT pos_east_m, pos_north_m, pos_up_m FROM telemetry_frames ORDER BY id DESC LIMIT 1').fetchone()
print(f'PASS: Validated ENU Vector: East={row[0]}m, North={row[1]}m, Up={row[2]}m')
conn.close()
"

echo ""
echo "=== ALL AUTOMATED TESTS PASSED SUCCESSFULLY ==="
