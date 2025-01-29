# GoalsARMPython
Python client for the Goals ARM model. Uses the model calculation engine from the GoalsARM repository.

## Installation
Clone the repo, and install it via uv

```console
uv build
```

## Development

### Prerequisites

For development, you'll need to install
* [Boost](https://www.boost.org/users/download/) (>=1.8.2, <=1.8.5) installed. The easiest way I find to do this, on windows, is to install one of the prebuilt binaries linked from the download page.
* [uv](https://docs.astral.sh/uv/) which is used to manage the project
* [CMake](https://cmake.org/) (>=3.15) for compiling the C++ code
* Python (>=3.10), you can [use uv to install this](https://docs.astral.sh/uv/guides/install-python/). You'll need development headers to compile the C++ code.

Note that when you run a `uv` command for the first time the C++ code will be compiled. But you will have to re-compile manually to pull in any changes. The python code will be installed in development mode, so any changes you make will be picked up automatically. But any changes to the C++ code will require a manual recompilation.

We're using [scikit-build-core](https://scikit-build-core.readthedocs.io/en/stable/index.html) for compiling the C++ code. This uses CMake to compile and should manage fetching any C++ dependencies (boost, GoalsARM source) and building the Python bindings.

### Create/activate the virtual environment

To create the venv

```console
uv sync
```

Then to activate it, on Windows via command prompt or powershell

```console
.venv\Scripts\activate
```

or on Linux

```console
source .venv/bin/activate
```

### Compile the C++ code

Note that first time you use a `uv` command it will compile the C++ code for you, but you will need to manually recompile if you make any changes to the C++ code. You can do this by passing `--reinstall` arg to any command. For example

```console
uv sync --reinstall
```

or

```console
uv run --reinstall pytest
```

or just the current pacakge

```console
uv run --reinstall-package goals pytest
```

By default, the C++ code will be compiled in release mode (with optimisations) and using GoalsARM from GitHub.

### Release/Debug

You can pass args to compile in debug mode

```console
DEBUG_BUILD=true uv run --reinstall-package goals pytest
```

or

```console
uv run scripts/compile.py --debug
```

### Local/GitHub

or against local sources

```console
LOCAL_BUILD=true uv run --reinstall-package goals pytest
```

or

```console
uv run scripts/compile.py --local
```

You will need to set the path to your local sources by changing `GOALS_ARM_PATH` in `pyproject.toml`. You need to use a fully qualified path for this.

Note that when compiling against non-local sources, CMake will fetch the main branch of GoalsARM from GitHub. You can configure this by changing `GOALS_ARM_GIT_TAG` in `pyproject.toml`.

These can be combined e.g.

```console
uv run scripts/compile.py --debug --local
```

### Run the tests

Note that any changes to the Python code will be picked up automatically, but you will need to recompile the C++ code manually if there are any changes. You can do this with the `--reinstall` or `--reinstall-package goals` flags.

```console
uv run pytest
```

### Running scripts

You'll need to run these from within the `uv`.

```console
uv run ./scripts/calibrate.py
uv run ./scripts/simulate.py
```

### Run coverage

Run tests analysing code coverage.

```console
uv run pytest --cov --cov-config=pyproject.toml
```

## Run lint

This will use [ruff](https://docs.astral.sh/ruff/). Configure settings in `pyproject.toml`

```console
uvx ruff check
```

To automatically format the code
```console
uvx ruff format
```

### IDE integration

#### VSCode

* Install the Python extension from Microsoft

If you are only developing the Python code, this is fairly straightforward.

1. Open the folder in VSCode
1. Create the virtual environment with `uv`, from a terminal in VSCode run `uv sync`. This will create a virtual environment `.venv`, install dependencies and compile the C++ code.
1. You now need to point VSCode to the Python interpreter managed by `uv`, there are two ways
   * Open the command palette (Ctrl+Shift+P) and run "Python: Select Interpreter" to the version of Python from your virtual env. It should be something like `.venv/bin/python` or `.venv\Scripts\python` on Windows. You may need to restart VSCode after creating the venv in step 2.
   * or, open the command palette (Ctrl+Shift+P) and run "Python: Create Environment", select "Venv" type, then select "GoalsARMPython". Note that this should be the existing venv, you should not recreate the environment afresh.
1. You should now be able to run and debug the Python tests and code from the IDE. Changes to Python code will be picked up automatically, but note that if you want to update any of the C++ you will need to recompile. To do so run `uv sync --reinstall` or `uv sync --reinstall-package goals` from the terminal.
1. This will pull and install GoalsARM C++ code from GitHub. You can change the branch if you want by setting `GOALS_ARM_GIT_TAG` in `pyproject.toml` and recompiling via `uv sync --reinstall`

Note that as this file contains a CMakeLists.txt your IDE might try and interpret this project as a CMake project. This will not compile as a raw CMake project, it requires scikit-build-core to compile succesfully. If you are using the CMake Tools VSCode extension, you can stop this by adding the following to your `.vscode/settings.json`.

```
{
    "cmake.automaticReconfigure": false,
    "cmake.configureOnOpen": false,
    "cmake.autoSelectActiveFolder": false,
    "cmake.sourceDirectory": "",
    "cmake.ignoreCMakeListsMissing": true
}
```

If you want to debug your a local copy of GoalsARM C++ code we need to do some more setup.

1. Install the [Python & C++ Debugger](https://marketplace.visualstudio.com/items?itemName=benjamin-simmonds.pythoncpp-debug) extension
1. Add the GoalsARM package to this VSCode workspace "File" -> "Add folder to Workspace..."/ (note that this won't work if you open GoalsARM and add GoalsARMPython to the workspace. You must open GoalsARMPython first)
1. If you don't already have one, create a `launch.json` by following the steps [here](Open the command palette (Ctrl+Shift+P) and run "Python: Select interpreter") 
1. On Windows, add the following configuration to your `.vscode/launch.json`
   ```
   {
       "version": "0.2.0",
       "configurations": [
           {
               "name": "Python C++ Debugger",
               "type": "pythoncpp",
               "request": "launch",
               "pythonConfig": "default",
               "cppConfig": "default (win) Attach"
           },
       ]
   }
   ```
   On Linux, swap the "cppConfig" for "default (gdb) Attach".
1. Set the path to the root of your local checkout of GoalsARM by setting the value of `GOALS_ARM_PATH` in the `pyproject.toml`
1. Recompile the code for debugging, `uv run scripts/compile.py --debug --local`. This will compile with debug symbols and link it to your local copy.
1. You should now be able to set breakpoints, in any of the GoalsARMPython code or the GoalsARM code.
1. To run it, open the "Run and debug" tab in VSCode, open the file you want to debug. Check the "Python C++ Debugger" is selected at the top and click the play button to start the debugger. This will launch a Python debugger and a C++ debugger and attach to it using the process ID of the Python debugger.

##### Testing

To have the Python and C++ debugger work from tests requires more configuration. By default the Python extension makes the test runner and test debug available to you. If you only want to debug the Python code, this will work fine. If you want to debug the C++ code also, this is not possible at the moment with the Python & C++ debugger extension. Easest way to achieve this is create a temporary file in `scripts` which calls your test e.g.

```python
import pytest


if __name__ == "__main__":
    pytest.main()
```

You can pass args to `pytest.main` to run a single file e.g. to run just `"tests/test_goals_excel.py"`, call `pytest.main(["tests/test_goals_excel.py"])`. Then run this via "Run and Debug` described in the section above.
