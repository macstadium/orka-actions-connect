#!/bin/bash

mkdir -p /Users/$(echo $(whoami))/agent
cp runner_connect.py /Users/$(echo $(whoami))/agent/
cp runner_connect.cfg /Users/$(echo $(whoami))/agent/

