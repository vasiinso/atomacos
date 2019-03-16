#!/usr/bin/env bash
if [[ $TRAVIS_BRANCH = "master" ]]; then
    if [[ $TRAVIS_PULL_REQUEST = "false" ]]; then
        rm -rfv dist/*
        git config --global user.name "semantic-release (via TravisCI)"
        git config --global user.email "semantic-release@travis"
        pip install python-semantic-release
        if semantic-release version --noop | grep bumped; then
            echo "Deploying"
            semantic-release publish
            flit publish
        else
            echo "Skipping"
        fi
    fi
fi
