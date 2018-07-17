fuser -k $1/tcp || true
PID=$!
sleep 1
kill -9 $PID
