# Web-App

Flask clothing store web application for group project.

## Installation

1. Clone this repository and `cd` into it
2. Create a python virtual environment in the root directory

```shell
python3 -m venv .venv
```

3. Activate the virtual environment

   - The invocation of the activation script is platform-specific, you can check the [venv docs](https://docs.python.org/3/library/venv.html#how-venvs-work) for more information. See below for [activation examples](#activation-examples) of activation on common platforms/shells.

4. Lastly, install the dependencies for the appliction

```shell
pip3 install Flask
```

### Activation examples

_I have not tested if the Windows commands work_

#### bash/zsh (Linux & Mac)

```bash
source .venv/bin/activate
```

#### Windows PowerShell

```powershell
PS C:\> .venv\Scripts\Activate.ps1
```

#### Windows cmd.exe

```cmd
C:\> .venv\Scripts\activate.bat
```

## Running the application

1. Make sure the python virtual environment is activated (see above)

2. Initialize the database

```
flask --app clothing_store init-db
```

3. Run the application, the `--debug` option will automatically rerun the application when files change. However, you will still have to refresh the browser to see the changes.

```
flask --app clothing_store run --debug
```

4. Open the web app in a browser at http://localhost:5000

## Development

### Testing

First install the testing tools `pytest` and `coverage` in your virtual environment

```
pip install pytest coverage
```

#### Pytest

1. For testing with `pytest` to work you will need to install the clothing store application with `pip`. Make sure you are in the root project directory `Web-App` and your virtual environment is activated.

```
pip install -e .
```

2. Then just run `pytest`

#### Coverage

To measure code coverage of the tests, use the `coverage` command to run `pytest` instead of running it directly.

```
coverage run -m pytest
```

## Overall tips:

- Always make sure you are in the root directory `Web-App` and the virtual environment is active.
  - To check if the virtual environment is active run `which python`, this should print out a path to the projects virtual environment somewhere in the root `Web-App` directory if the virtual environment is active
- If you are ever using a new terminal (like turning off the computer or opening a new terminal), you will need to re-activate the virtual environment before running any commands like, for example, starting the development server
