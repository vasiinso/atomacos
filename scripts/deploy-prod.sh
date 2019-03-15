#!/usr/bin/env bash
if [[ $TRAVIS_BRANCH = "master" ]]; then
    if [[ $TRAVIS_PULL_REQUEST = "false" ]]; then
        rm -rfv dist/*
        git config --global user.name "semantic-release (via TravisCI)"
        git config --global user.email "semantic-release@travis"
        pip install python-semantic-release
        if semantic-release version | grep Bump; then
            echo "Deploying"
            flit publish
            semantic-release changelog --post
        else
            echo "Skipping"
        fi
    fi
fi
