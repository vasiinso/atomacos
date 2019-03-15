# Contributing

Thanks for being interested in contributing to this project.

Please follow these:
- [GitHub flow]
- Make sure [tox] passes
- Write tests for new features or fixes.
  - Tests for this project can be hard,
    especially when AX API is involved.
- Follow [angular commit] style message

*Notes:*
Run `tox -e checkpermissions` to see what needs AX permission.
Remember to revoke permission when it's no longer needed.

## Commit Messages
- Follow [angular commit format][angular commit]
- This helps with auto-deploying from master


## pre-commit
[Pre-commit] is configured
- [black] to format your code
- [flake8] for extra linting

[angular commit]: https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#commits
[tox]: https://tox.readthedocs.io/en/latest/
[black]: https://github.com/ambv/black
[flake8]: http://flake8.pycqa.org/en/latest/
[pre-commit]: https://pre-commit.com/
[github flow]: https://guides.github.com/introduction/flow/
