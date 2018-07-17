fuser -k $1/tcp || true
PID=$!
kill -INT $PID
