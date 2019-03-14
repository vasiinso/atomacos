echo $1
python -m pip install bump2version
echo $(bumpversion --dry-run --list minor | grep new_version | sed s,'^.*=',,).dev${TRAVIS_BUILD_NUMBER} patch
python -m flit publish
