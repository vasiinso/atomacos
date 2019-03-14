echo $1
echo $(bumpversion --dry-run --list minor | grep new_version | sed s,'^.*=',,).dev${TRAVIS_BUILD_NUMBER} patch
flit publish
