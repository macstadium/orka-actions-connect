sudo docker run -d --restart always --name github-runner \
  -e REPO_URL="<your-repo-url>" \
  -e RUNNER_NAME="master-runner" \
  -e RUNNER_TOKEN="<your-runner-token>" \
  -e RUNNER_WORKDIR="</tmp/github-runner-your-repo>" \
  -e RUNNER_GROUP="<your-group>" \
  -e LABELS="master" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /tmp/github-runner-your-repo:/tmp/github-runner-your-repo \
  myoung34/github-runner:latest