#!/bin/bash

run() {
  echo 'Content-type: text/plain'
  echo

  whoami
  pwd

  export STOGRADE_SHARE="$(mktemp -d)"
  echo STOGRADE_SHARE: $STOGRADE_SHARE

  cp -rv /home/referee/.local/share/stograade/* $STOGRADE_SHARE/

  command="/usr/bin/docker run -v $(readlink -f $STOGRADE_SHARE):/stograde_share/ -v $(readlink -f /home/referee/.ssh/):/stograde_share/.ssh/ --env-file /home/referee/gmail_auth.sh -i stodevx/stograde:HEAD"

  echo "docker command: $command"

  cat - | $command referee --debug --stdin --send 2>&1

  echo "res code: $?"
  echo "done with referee"

  echo "doing some cleanup in the container"

  $command rm -rfv /stograde_share/data/specs/_cache/ 2>&1
  echo "res code: $?"
  $command rm -rfv /stograde_share/students 2>&1
  echo "res code: $?"

  echo "now doing the rest of the cleanup"
  rm -rfv $STOGRADE_SHARE
}

cat - | run 2>&1 | tee -a /home/referee/stograade-cgi.log
