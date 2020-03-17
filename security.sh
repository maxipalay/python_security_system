# auto-restarting script taken from
# https://stackoverflow.com/questions/696839/how-do-i-write-a-bash-script-to-restart-a-process-if-it-dies


#!/bin/sh

while true; do
  nohup python3 security_system.py > output.txt
done &
