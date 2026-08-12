#!/bin/sh

mkdir -p /data/plugins

if [ ! -f /data/paper.jar ]; then
    cp /server/paper.jar /data/paper.jar
fi

cp /server/plugins/*.jar /data/plugins/

if [ ! -f /data/eula.txt ]; then
    echo "eula=true" > /data/eula.txt
fi

# Start fake HTTP server in background so Render's health check passes
python3 /server.py &

exec java \
    -Xms256M \
    -Xmx350M \
    -XX:+UseG1GC \
    -XX:+ParallelRefProcEnabled \
    -XX:MaxGCPauseMillis=200 \
    -jar /data/paper.jar \
    --nogui