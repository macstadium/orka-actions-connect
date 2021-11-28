#!/bin/bash

export USER=$(curl -s "http://169.254.169.254/metadata/github_user" | \
	python3 -c "import sys, json; print(json.load(sys.stdin)['value'])")
export REPO=$(curl -s "http://169.254.169.254/metadata/github_repo_name" | \
	python3 -c "import sys, json; print(json.load(sys.stdin)['value'])")

vm_name=$(curl -s "http://169.254.169.254/metadata/vm_name" | \
	python3 -c "import sys, json; print(json.load(sys.stdin)['value'])")
pat=$(curl -s "http://169.254.169.254/metadata/github_pat" | \
	python3 -c "import sys, json; print(json.load(sys.stdin)['value'])")
repo_url="https://github.com/$USER/$REPO"

runner_token=$(curl \
-XPOST \
-H"Accept: application/vnd.github.v3+json" \
-H"authorization: Bearer $pat" \
"https://api.github.com/repos/$USER/$REPO/actions/runners/registration-token" | \
	python3 -c "import sys, json; print(json.load(sys.stdin)['token'])")

./config.sh --url $repo_url --token $runner_token --name $vm_name --unattended --work "_work" --labels $vm_name
./svc.sh install
./svc.sh start
