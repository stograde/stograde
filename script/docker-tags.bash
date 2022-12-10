#!/bin/bash

suffix="$1"

if [[ $TRIGGER == "push" && $GITHUB_REF == "refs/heads/main" ]]
then
  tags="$tags $DOCKER_IMAGE:HEAD$suffix"
fi

if [[ $TRIGGER == "push" && $GITHUB_REF =~ refs/heads/.*gh-actions.* ]]
then
  tags="$tags $DOCKER_IMAGE:$GITHUB_SHA$suffix"
fi

if [[ $GITHUB_REF =~ refs/tags/v.* ]]
then
  tags="$tags $DOCKER_IMAGE:${GITHUB_REF#refs/tags/}$suffix"
  if [[ $TRIGGER == "release" ]]
  then
    tags="$tags $DOCKER_IMAGE:latest$suffix"
  fi
fi

tags=$(echo "${tags# }" | tr " " ",")

echo "::set-output name=tags::$tags"
