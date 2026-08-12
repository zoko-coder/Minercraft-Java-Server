#!/bin/sh

mkdir -p /data/plugins

if [ ! -f /data/paper.jar ]; then
    cp /server/paper.jar /data/paper.jar
fi

cp /server/plugins/*.jar /data/plugins/

if [ ! -f /data/eula.txt ]; then
    echo "eula=true" > /data/eula.txt
fi

exec java \
    -Xms350M \
    -Xmx400M \
    -jar /data/paper.jar \
    --nogui