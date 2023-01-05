#!/bin/bash

source .env

mkdir -p logs

ps -ef | grep oracle.py | head -1 | awk '{print $2}' | xargs kill || true
#ps -ef | grep monitor.py | head -1 | awk '{print $2}' | xargs kill

nohup python3 src/oracle.py &
#nohup flask run &