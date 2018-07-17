fuser -k $1/tcp || true
PID=$!
sleep 1
kill -INT $PID
