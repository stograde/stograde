#!/bin/bash

suffix="$1"

if [[ $GITHUB_REF == "ref/heads/master" ]]
then
  tags="$tags $DOCKER_IMAGE:HEAD$suffix"
fi

if [[ $GITHUB_REF =~ ref/heads/travis-.* ]]
then
  tags="$tags $DOCKER_IMAGE:$GITHUB_SHA$suffix"
fi

if [[ $GITHUB_REF == "refs/heads/migrate-to-gh-actions" ]]
then
  tags="$tags $DOCKER_IMAGE:$GITHUB_SHA$suffix"
  tags="$tags $DOCKER_IMAGE:HEAD$suffix"

fi

if [[ $GITHUB_REF =~ ref/tags/v.* ]]
then
  tags="$tags $DOCKER_IMAGE:${GITHUB_REF#refs/tags/}$suffix"
  if [[ "$(script/github-latest-release)" == "${GITHUB_REF#refs/tags/}" ]]
  then
    tags="$tags $DOCKER_IMAGE:latest$suffix"
  fi
fi

tags=$(${tags# } | tr " " ",")

echo "::set-output name=tags::$tags"
