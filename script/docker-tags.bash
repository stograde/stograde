#!/bin/bash

ref="$1"
suffix="$2"

if [[ "$ref" == "ref/heads/master" ]]
then
  deploy_targets="$deploy_targets $DOCKER_IMAGE:HEAD$suffix"
fi

if [[ "$ref" =~ ref/heads/travis-.* ]]
then
  deploy_targets="$deploy_targets $DOCKER_IMAGE:$GITHUB_SHA$suffix"
fi

if [[ "$ref" == "refs/heads/migrate-to-gh-actions" ]]
then
  deploy_targets="$deploy_targets $DOCKER_IMAGE:$GITHUB_SHA$suffix"
fi

if [[ "$ref" =~ ref/tags/v.* ]]
then
  deploy_targets="$deploy_targets $DOCKER_IMAGE:$TRAVIS_TAG$suffix"
  if [[ "$(script/github-latest-release)" == "${ref#refs/tags/}" ]]
  then
    deploy_targets="$deploy_targets $DOCKER_IMAGE:latest$suffix"
  fi
fi

deploy_targets=${deploy_targets# }

echo "$deploy_targets"
