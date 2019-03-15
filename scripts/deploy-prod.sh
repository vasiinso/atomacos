#!/usr/bin/env bash
if [[ $TRAVIS_BRANCH = "master" ]]; then
    if [[ $TRAVIS_PULL_REQUEST = "false" ]]; then
        rm -rf dist/*
        git config --global user.name "semantic-release (via TravisCI)"
        git config --global user.email "semantic-release@travis"
        pip install python-semantic-release
        semantic-release version
        flit publish
        semantic-release changelog --post
    fi
fi
