#!/bin/bash

#export FLASK_APP=./src/monitor.py
export INFO_LOG=./logs/info.logs
export ERROR_LOG=./logs/error.logs

mkdir -p logs

ps -ef | grep oracle.py | head -1 | awk '{print $2}' | xargs kill
#ps -ef | grep monitor.py | head -1 | awk '{print $2}' | xargs kill

nohup python3 src/oracle.py &
#nohup flask run &