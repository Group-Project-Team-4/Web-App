# Web-App

Flask web application for group project. Please see [this file](https://github.com/Group-Project-Team-4/Web-App/blob/main/web-app-lab.md) for the lab instructions for end-to-end (E2E) testing.

## Installation

1. Clone this repository and `cd` into it
2. Create a python virtual environment in the root directory.

```shell
python3 -m venv .venv
```
3. Activate the virtual environment [according to your platform](https://docs.python.org/3/library/venv.html#how-venvs-work).

#### Activation examples:
**NOTE:** You will need to re-activate the virtual environment if your terminal is closed (shutting off PC, closing terminal app, etc.). Always ensure that the virtual environment is active before attempting to run the application, and always ensure that it is **NOT** active when you are not working with the application, but are still using the terminal.

Linux/Mac (bash/zsh/Any Bourne-compatible shell):
```shell
source .venv/bin/activate
```
Windows (PowerShell):
```shell
.venv\Scripts\Activate.ps1
```
Windows (cmd.exe):
```shell
.venv\Scripts\Activate.bat
```

4. Lastly, install the dependencies for the application

```sh
pip3 install -r requirements.txt
```

## Running the application

1. Make sure the python virtual environment is activated (see above)

2. Initialize the database

```sh
flask --app clothing_store init-db
```

3. Run the application, the `--debug` option will automatically rerun the application when files change. However, you will still have to refresh the browser to see the changes.

```sh
flask --app clothing_store run --debug
```

4. Open the web app in a browser at http://localhost:5000

## Development

### Testing

1. For testing with `pytest` to work you will need to install the clothing store application with `pip`. Make sure you are in the root project directory `Web-App` and your virtual environment is activated.

    ```sh
    pip install -e .
    ```

2. Follow [these lab instructions](https://github.com/Group-Project-Team-4/Web-App/blob/main/web-app-lab.md#tutorial) to learn a little bit about how to create and run end-to-end (E2E) testing for web applications.

    **OR**

2. From the root of the repository run the `pytest tests/pytest` command to run default test scripts.

    **IMPORTANT**: The `tests` directory also contains Selenium and API tests, which **ARE NOT** Pytest scripts. Running `pytest` on its own will cause it to source incompatible files, which will create errors and fail to run the actual test scripts. Anytime you want to run `pytest` or `coverage`, you **MUST** specify the `tests/pytest` directory in the command to make sure only the appropriate test scripts are sourced.

    ```sh
    pytest tests/pytest
    ```

#### Coverage

To measure code coverage of the tests, use the `coverage` command to run `pytest` instead of running it directly.

```
coverage run -m pytest tests/pytest
```

## Overall tips:

- When working with the application, always make sure you are in the root directory `Web-App` and the virtual environment is active.
- To check if the virtual environment is active, run `which python`, which should print out a path to the project's virtual environment in the root `Web-App` directory if the virtual environment is active
