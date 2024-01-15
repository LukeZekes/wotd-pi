#!/bin/bash
# Updates the local repository to the remote on github, once an internet connection has been established
REPO_DIR=$( cd -- $(dirname -- ${BASH_SOURCE[0]}) &> /dev/null && pwd )
while true; do
  PING_OUT=$(ping -c 1 github.com)
  if [[ $PING_OUT == *"1 packets transmitted, 1 received"* ]]; then
    cd -- $REPO_DIR
    git pull > launch_out.txt 2> launch_err.txt
    python main.py
    break;
  else
    sleep 1
  fi
done