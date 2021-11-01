#!/bin/bash

python3 -m ensurepip --upgrade
pip3 install requests
mkdir -p /Users/$(echo $(whoami))/agent
cp runner_connect.py /Users/$(echo $(whoami))/agent/
cp runner_connect.cfg /Users/$(echo $(whoami))/agent/

