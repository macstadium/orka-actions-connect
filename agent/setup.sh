#!/bin/bash

python3 -m pip install requests
mkdir -p /Users/$(echo $(whoami))/agent
cp runner_connect.py /Users/$(echo $(whoami))/agent/
cp runner_connect.cfg /Users/$(echo $(whoami))/agent/
cp com.orka-actions-connect.plist /Library/LaunchDaemons/
