# Contributing

This project is based on [Geronimo-iaa's Python Module Template](https://github.com/geronimo-iia/python-module-template).
This is a cookiecutter template for a typical Python library following modern packaging conventions. 
It utilizes popular libraries to fully automate all development and deployment tasks.


## Setup

### Requirements

You will need:

* Python 3.8"+
* [Pyenv](https://github.com/pyenv/pyenv#installation)
* [poetry](https://python-poetry.org/)
* Make


### Make Installation

A powerfull tool:
* macOS: `$ xcode-select --install`
* Linux: [https://www.gnu.org/software/make](https://www.gnu.org/software/make)
* Windows: [https://mingw.org/download/installer](https://mingw.org/download/installer)

### Pyenv Installation

Pyenv will manage all our python version.
Follow [https://github.com/pyenv/pyenv#installation](https://github.com/pyenv/pyenv#installation)


### Python Installation

 `$ pyenv install 3.8`


### Poetry Installation: [https://poetry.eustace.io/docs/#installation](https://poetry.eustace.io/docs/#installation)

Poetry will manage our dependencies and create our virtual environment for us.



## Make Target list


| Name                    | Comment                                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------------------- |
| make install            | Install project dependencies                                                                    |
| make configure          | Configure poetry                                                                                |
| make tag                | Create and push a tag based on current project version. This will launch github release action. |
| make next-patch-version | Increment patch version of the project.                                                         |
|                         |                                                                                                 |


## Poe Target list


| Name                    | Comment                                                                                  |
| ----------------------- | ---------------------------------------------------------------------------------------- |
| poetry poe check        | Run linters and static analysis                                                          |
| poetry poe test         | Run unit tests                                                                           |
| poetry poe build        | Builds the source and wheels archives (and run check & test target)                      |
| poetry poe publish      | Publishes the package, previously built with the build command, to the remote repository |
| poetry poe docs         | Builds  site documentation.                                                              |
| poetry poe docs-publish | Build and publish site documentation.                                                    |
| poetry poe clean        | Delete all generated and temporary files                                                 |
| poetry poe requirements | Generate requirements.txt                                                                |
|                         |                                                                                          |

You could retrieve those commands with `poetry poe`. It will output something like this :

```
Poe the Poet - A task runner that works well with poetry.
version 0.25.0

Result: No task specified.

USAGE
  poetry poe [-h] [-v | -q] [--root PATH] [--ansi | --no-ansi] task [task arguments]

GLOBAL OPTIONS
  -h, --help     Show this help page and exit
  --version      Print the version and exit
  -v, --verbose  Increase command output (repeatable)
  -q, --quiet    Decrease command output (repeatable)
  -d, --dry-run  Print the task contents but don't actually run it
  --root PATH    Specify where to find the pyproject.toml
  --ansi         Force enable ANSI output
  --no-ansi      Force disable ANSI output

CONFIGURED TASKS
  build          Build module
  publish        Publish module
  check          Run Linter
  test           Run unit tests
  docs           Build site documentation
  docs-publish   Publish site documentation
  clean          Remove all generated and temporary files
  requirements   Generate requirements.txt
```
