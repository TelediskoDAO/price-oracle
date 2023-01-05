#!/bin/bash

source environment

mkdir -p logs

ps -ef | grep oracle.py | head -1 | awk '{print $2}' | xargs kill || true
ps -ef | grep "flask run -p $FLASK_PORT" | head -1 | awk '{print $2}' | xargs kill || true

sleep 3

nohup python3 src/oracle.py &
nohup flask run -p $FLASK_PORT &