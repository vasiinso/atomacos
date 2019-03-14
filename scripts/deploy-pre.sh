#!/usr/bin/env bash
python -m pip install bump2version
bumpversion --new-version $(bumpversion --dry-run --list minor | grep new_version | sed s,'^.*=',,).dev${TRAVIS_BUILD_NUMBER} minor
rm -rf dist/*
flit publish
