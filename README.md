# Atomacos - Automated Testing on macOS
[![Build Status](https://travis-ci.org/daveenguyen/atomacos.svg?branch=master)](https://travis-ci.org/daveenguyen/atomacos)

This library is a fork of [atomac].
It was created to provide a release with python 3 support because
there has not been a release [since 2013](https://github.com/pyatom/pyatom/releases)


## Introduction
Atomacos is a library to enable GUI testing of macOS applications via the Apple Accessibility API.
Atomacos has direct access to the API via [pyobjc]. It's fast and easy to use to write tests.


## Getting started
Requirements
- macOS
- [pyobjc]
- Systemwide Accesibility enabled

On travis, it's only on 10.11 because we are able to enable accessibility API.

If you experience issues, please open a ticket in the [issue tracker][issues].

### Enabling Systemwide Accessibility
Check the checkbox:
`System Preferences > Universal Access > Enable access for assistive devices`
`System Preferences > Security & Privacy > Privacy > Accessibility`

Failure to enable this will result in `AXErrorAPIDisabled` exceptions during some module usage.


### Installing

For release
```bash
$ pip install atomacos
```

For pre-release
```bash
$ pip install --pre atomacos
```


## Usage
Once installed, you should be able to use it to launch an application:

```python
>>> import atomacos
>>> atomacos.launchAppByBundleId('com.apple.Automator')
```

This should launch Automator.


Next, get a reference to the UI Element for the application itself:

```python
>>> automator = atomacos.getAppRefByBundleId('com.apple.Automator')
>>> automator
<atomacos.AXClasses.NativeUIElement AXApplication Automator>
```


Now, we can find objects in the accessibility hierarchy:

```python
>>> window = automator.windows()[0]
>>> window.AXTitle
u'Untitled'
>>> sheet = window.sheets()[0]
```

Note that we retrieved an accessibility attribute from the Window object - `AXTitle`.
Atomacos supports reading and writing of most attributes.
Xcode's included `Accessibility Inspector` can provide a quick way to find these attributes.


There is a shortcut for getting the sheet object which
bypasses accessing it through the Window object.
Atomacos can search all objects in the hierarchy:

```python
>>> sheet = automator.sheetsR()[0]
```


There are search methods for most types of accessibility objects.
Each search method, such as `windows`,
has a corresponding recursive search function, such as `windowsR`.

The recursive search finds items that aren't just direct children, but children of children.
These search methods can be given terms to identify specific elements.
Note that `*` and `?` can be used as wildcard match characters in all search methods:

```python
>>> close = sheet.buttons('Close')[0]
```


There are methods to search for UI Elements that match any number of criteria.
The criteria are accessibility attributes:

```python
>>> close = sheet.findFirst(AXRole='AXButton', AXTitle='Close')
```

`findFirst` and `findFirstR` return the first item found to match the criteria or `None`.
`findAll` and `findAllR` return a list of all items that match the criteria or an empty list(`[]`).


Objects are fairly versatile.
You can get a list of supported attributes and actions on an object:

```python
>>> close.getAttributes()
[u'AXRole', u'AXRoleDescription', u'AXHelp', u'AXEnabled', u'AXFocused',
u'AXParent', u'AXWindow', u'AXTopLevelUIElement', u'AXPosition', u'AXSize',
u'AXTitle']
>>> close.AXTitle
u'Close'
>>> close.getActions()
[u'Press']
```


Performing an action is as natural as:

```python
>>> close.Press()
```

Any action can be triggered this way.



# Todo
- LDTP
    - Maybe extract into its own project and use atomacos at the backend.
- Better mouse handling.
    - For example, a method to smoothly drag from one UI Element to another.
- Cleanup the search methods
    - We could use currying to define all the search methods in AXClasses in a cleaner way.


# Links
- [License]
- [Issues]
- [Source] Code
- Changes
    - [Commits] page has all changes to the project.
    - [Release] page will also outline changes
- Thanks [ATOMac] and [PyObjC]


[source]:  https://github.com/daveenguyen/atomacos
[release]: https://github.com/daveenguyen/atomacos/releases
[commits]: https://github.com/daveenguyen/atomacos/commits
[license]: https://github.com/daveenguyen/atomacos/blob/master/LICENSE
[issues]:  https://github.com/daveenguyen/atomacos/issues
[atomac]:  https://github.com/pyatom/pyatom
[pyobjc]:  https://bitbucket.org/ronaldoussoren/pyobjc
