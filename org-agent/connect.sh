#!/bin/bash

org=$(curl -s "http://169.254.169.254/metadata/github_org" | \
        python3 -c "import sys, json; print(json.load(sys.stdin)['value'])")
vm_name=$(curl -s "http://169.254.169.254/metadata/orka_vm_name" | \
        python3 -c "import sys, json; print(json.load(sys.stdin)['value'])")
# NOTE: GitHub personal access token (github_pat) must have `admin:org` permissions
pat=$(curl -s "http://169.254.169.254/metadata/github_pat" | \
        python3 -c "import sys, json; print(json.load(sys.stdin)['value'])")
org_url="https://github.com/$org"

runner_token=$(curl \
-XPOST \
-H"Accept: application/vnd.github.v3+json" \
-H"authorization: Bearer $pat" \
"https://api.github.com/orgs/$org/actions/runners/registration-token" | \
        python3 -c "import sys, json; print(json.load(sys.stdin)['token'])")

cd /Users/admin/agent/
./config.sh --url $org_url --token $runner_token --runnergroup "Default" --name $vm_name --work "_work" --labels $vm_name
./svc.sh install
./svc.sh start
