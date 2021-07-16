## api-server-flask

`api-server-flask` is a boilerplate starter template designed to help you quickstart your Flask based REST API server development. It has all the ready-to-use bare minimum essentials.


## Features

- APIs: Signup, Login with (email, password), Logout, Edit User
- SQLAlchemy + SQLite
- Configs
- Requirements
- Tests: SignUp, Login


## Table of Contents

1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [Modules](#modules)
4. [Testing](#testing)


## Getting Started

clone the project

```bash
$ git clone https://github.com/app-generator/api-server-flask.git
$ cd api-server-flask
```

create virtual environment using python3 and activate it (keep it outside our project directory)

```bash
$ python3 -m venv /path/to/your/virtual/environment
$ source <path/to/venv>/bin/activate
```

install dependencies in virtualenv

```bash
$ pip install -r requirements.txt
```

setup `flask` command for our app

```bash
$ export FLASK_APP=run.py
$ export FLASK_ENV=development
```

> Or for Windows-based systems

```powershell
$ (Windows CMD) set FLASK_APP=run.py
$ (Windows CMD) set FLASK_ENV=development
$
$ (Powershell) $env:FLASK_APP = ".\run.py"
$ (Powershell) $env:FLASK_ENV = "development"
```

initialize database, check `run.py` for shell context

```bash
$ flask shell
>>> from api import db
>>> db.create_all()
```

start test APIs server at `localhost:5000`

```bash
$ python run.py
```
or 
```bash
$ flask run
```

use `flask-restx`' swagger dashboard to test APIs, or alternatively use `postman`


## Project Structure

```bash
api-server-flask/
├── api
│   ├── config.py
│   ├── __init__.py
│   ├── models.py
│   └── routes.py
├── Dockerfile
├── README.md
├── requirements.txt
├── run.py
└── tests.py
```


## Modules

This application uses the following modules

 - Flask==1.1.4
 - flask-restx==0.4.0
 - Flask-JWT-Extended
 - pytest


## Testing

Run tests using `pytest tests.py`
