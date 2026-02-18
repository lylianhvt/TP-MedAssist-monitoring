#!/bin/bash
set -e
BACKUP_DIR="/backup"
BACKUP_FILE="$BACKUP_DIR/medassist-$(date +%Y%m%d%H%M%S).sql"
START=$(date +%s)
mkdir -p "$BACKUP_DIR"

mysqldump -h mysql -u medassist -pmedassist medassist > "$BACKUP_FILE" 2>/tmp/backup_error.log && STATUS=0 || STATUS=1
SIZE=$(stat -c %s "$BACKUP_FILE" 2>/dev/null || echo 0)
DURATION=$(($(date +%s) - $START))
TIMESTAMP=$(date +%s)

cat <<EOF | curl --data-binary @- http://pushgateway:9091/metrics/job/mysql_backup
# TYPE mysql_backup_status gauge
mysql_backup_status $STATUS
# TYPE mysql_backup_size_bytes gauge
mysql_backup_size_bytes $SIZE
# TYPE mysql_backup_duration_seconds gauge
mysql_backup_duration_seconds $DURATION
# TYPE mysql_backup_last_timestamp gauge
mysql_backup_last_timestamp $TIMESTAMP
EOF

exit $STATUS
