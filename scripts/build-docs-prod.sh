#!/usr/bin/env bash
if [[ $TRAVIS_BRANCH = "master" ]]; then
    if [[ $TRAVIS_PULL_REQUEST = "false" ]]; then
        tox -e docs --installpkg dist/*.whl
    fi
fi
