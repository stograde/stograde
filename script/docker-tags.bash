#!/bin/bash

suffix="$1"

if [[ $GITHUB_REF == "ref/heads/master" ]]
then
  deploy_targets="$deploy_targets $DOCKER_IMAGE:HEAD$suffix"
fi

if [[ $GITHUB_REF =~ ref/heads/travis-.* ]]
then
  deploy_targets="$deploy_targets $DOCKER_IMAGE:$GITHUB_SHA$suffix"
fi

if [[ $GITHUB_REF == "refs/heads/migrate-to-gh-actions" ]]
then
  deploy_targets="$deploy_targets $DOCKER_IMAGE:$GITHUB_SHA$suffix"
fi

if [[ $GITHUB_REF =~ ref/tags/v.* ]]
then
  deploy_targets="$deploy_targets $DOCKER_IMAGE:$TRAVIS_TAG$suffix"
  if [[ "$(script/github-latest-release)" == "${GITHUB_REF#refs/tags/}" ]]
  then
    deploy_targets="$deploy_targets $DOCKER_IMAGE:latest$suffix"
  fi
fi

deploy_targets=${deploy_targets# }

echo "$deploy_targets"
