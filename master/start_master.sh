sudo docker run -d --restart always --name github-runner \
  -e REPO_URL="https://github.com/jeff-vincent/orka-actions-spin-up" \
  -e RUNNER_NAME="master-runner" \
  -e RUNNER_TOKEN="AIJKXW6C6GNR7G7WB46H4TTA6N324" \
  -e RUNNER_WORKDIR="/tmp/github-runner-your-repo" \
  -e RUNNER_GROUP="your-group" \
  -e LABELS="master" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /tmp/github-runner-your-repo:/tmp/github-runner-your-repo \
  myoung34/github-runner:latest