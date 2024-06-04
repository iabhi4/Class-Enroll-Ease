#!/bin/bash

# Check if ports are provided as arguments
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 port1 port2 port3 ..."
    exit 1
fi

# Iterate over provided ports and kill the processes
for port in "$@"; do
    echo "Killing process on port $port..."
    pid=$(lsof -t -i :$port)
    if [ -n "$pid" ]; then
        kill -9 "$pid"
        echo "Process killed."
    else
        echo "No process found on port $port."
    fi
done

echo "Script completed."
