#!/bin/bash

user=$(curl -s "http://169.254.169.254/metadata/github_user" | \
        python3 -c "import sys, json; print(json.load(sys.stdin)['value'])")
repo=$(curl -s "http://169.254.169.254/metadata/github_repo_name" | \
        python3 -c "import sys, json; print(json.load(sys.stdin)['value'])")
vm_name=$(curl -s "http://169.254.169.254/metadata/orka_vm_name" | \
        python3 -c "import sys, json; print(json.load(sys.stdin)['value'])")
pat=$(curl -s "http://169.254.169.254/metadata/github_pat" | \
        python3 -c "import sys, json; print(json.load(sys.stdin)['value'])")
repo_url="https://github.com/$user/$repo"

runner_token=$(curl \
-XPOST \
-H"Accept: application/vnd.github.v3+json" \
-H"authorization: Bearer $pat" \
"https://api.github.com/repos/$user/$repo/actions/runners/registration-token" | \
        python3 -c "import sys, json; print(json.load(sys.stdin)['token'])")

cd /Users/admin/agent/
./config.sh --url $repo_url --token $runner_token --runnergroup "Default" --name $vm_name --work "_work" --labels $vm_name
./svc.sh install
./svc.sh start
