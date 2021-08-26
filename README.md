## Flask API Server

Flask Starter with JWT authentication, and **SQLite** persistance - Provided by **AppSeed** [App Generator](https://appseed.us/app-generator).
It has all the ready-to-use bare minimum essentials.

<br />

> Features:

- [API Definition](https://docs.appseed.us/boilerplate-code/api-unified-definition) - the unified API structure implemented by this server
- Simple, intuitive codebase - can be extended with ease. 
- Flask-restX, Flask-jwt_extended
- Docker, Unitary tests

<br />

> **[PRO Version](https://github.com/app-generator/api-server-flask-pro)** available: MongoDB persistance, Docker, Unitary Tests, 24/7 LIVE Support via [Discord](https://discord.gg/fZC6hup)

> Can be used with other [React Starters](https://appseed.us/apps/react) for a complete **Full-Stack** experience:

| [React Node JS Berry](https://appseed.us/product/react-node-js-berry-dashboard) | [Full-Stack Material PRO](https://appseed.us/full-stack/react-material-dashboard) | [React Node Datta Able](https://github.com/app-generator/react-datta-able) |
| --- | --- | --- |
| [![React Node JS Berry](https://user-images.githubusercontent.com/51070104/124934742-aa392300-e00d-11eb-83bf-28d8b8704ec8.png)](https://appseed.us/product/react-node-js-berry-dashboard) | [![Full-Stack Material PRO](https://user-images.githubusercontent.com/51070104/128878037-50da7a12-787d-455d-933a-30b2957e2896.png)](https://appseed.us/full-stack/react-material-dashboard) | [![React Node Datta Able](https://user-images.githubusercontent.com/51070104/125737710-834a9e6f-c39b-4f3b-a42a-9583ce2ce1da.png)](https://github.com/app-generator/react-datta-able)

<br />

![Flask API Server - Open-source Flask Starter provided by AppSeed.](https://user-images.githubusercontent.com/51070104/126349643-264d4cf4-6d0b-4c24-8185-adf69409fa4e.png)

<br />

## Table of Contents

1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [Modules](#modules)
4. [Testing](#testing)

## How to use the code

**Step #1** - Clone the project

```bash
$ git clone https://github.com/app-generator/api-server-flask.git
$ cd api-server-flask
```

**Step #2** - create virtual environment using python3 and activate it (keep it outside our project directory)

```bash
$ python3 -m venv /path/to/your/virtual/environment
$ source <path/to/venv>/bin/activate
```

**Step #3** - Install dependencies in virtualenv

```bash
$ pip install -r requirements.txt
```

**Step #4** - setup `flask` command for our app

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

**Step #5** - initialize database, check `run.py` for shell context

```bash
$ flask shell
>>> from api import db
>>> db.create_all()
```

**Step #6** - start test APIs server at `localhost:5000`

```bash
$ python run.py
```
or 
```bash
$ flask run
```

**Step #7** - use `flask-restx`' swagger dashboard to test APIs, or use `POSTMAN`

<br />

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

<br />

## Modules

This application uses the following modules

 - Flask==1.1.4
 - flask-restx==0.4.0
 - Flask-JWT-Extended
 - pytest

## Testing

Run tests using `pytest tests.py`

<br />

---
Flask API Server - provided by AppSeed [App Generator](https://appseed.us)
