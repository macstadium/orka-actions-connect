#!/bin/bash

python3 -m pip install requests
mkdir -p /Users/admin/agent
cp runner_connect.py /Users/admin/agent/
cp runner_connect.cfg /Users/admin/agent/
cp com.orka-actions-connect.plist /Library/LaunchDaemons/
