#!/bin/bash

run() {
  echo 'Content-type: text/plain'
  echo

  whoami
  pwd

  export CS251TK_SHARE="$(mktemp -d)"
  echo CS251TK_SHARE: $CS251TK_SHARE

  cp -rv /home/referee/.local/share/cs251tk/* $CS251TK_SHARE/

  command="/usr/bin/docker run -v $(readlink -f $CS251TK_SHARE):/cs251tk_share/ -v $(readlink -f /home/referee/.ssh/):/cs251tk_share/.ssh/ --env-file /home/referee/gmail_auth.sh -i stodevx/cs251-toolkit:HEAD"

  echo "docker command: $command"

  cat - | $command referee --debug --stdin --send 2>&1

  echo "res code: $?"
  echo "done with referee"

  echo "doing some cleanup in the container"

  $command rm -rfv /cs251tk_share/data/specs/_cache/ 2>&1
  echo "res code: $?"
  $command rm -rfv /cs251tk_share/students 2>&1
  echo "res code: $?"

  echo "now doing the rest of the cleanup"
  rm -rfv $CS251TK_SHARE
}

cat - | run 2>&1 | tee -a /home/referee/cs251tk-cgi.log
