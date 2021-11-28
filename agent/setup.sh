#!/bin/bash

python3 -m pip install requests
mkdir -p /Users/admin/agent
cp connect.sh /Users/admin/agent/
cp svc.sh /Users/admin/agent/
sudo cp com.orka-actions-connect.plist /Library/LaunchDaemons/
cd /Users/admin/agent/
curl -o actions-runner-osx-x64-2.284.0.tar.gz \
	-L https://github.com/actions/runner/releases/download/v2.284.0/actions-runner-osx-x64-2.284.0.tar.gz
tar xzf ./actions-runner-osx-x64-2.284.0.tar.gz
