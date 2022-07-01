## Flask API Server

Simple [Flask API Boilerplate](https://appseed.us/boilerplate-code/flask-api-boilerplate) enhanced with JWT authentication, SqlAlchemy, **SQLite** persistence and deployment scripts via Docker - Provided by **AppSeed**. It has all the ready-to-use bare minimum essentials.

<br />

> Features:

- `Up-to-date dependencies` 
- [API Definition](https://docs.appseed.us/boilerplate-code/api-unified-definition) - the unified API structure implemented by this server
- Simple, intuitive codebase - can be extended with ease. 
- `Flask-restX`, `Flask-jwt_extended`
- **Docker**, `Unitary tests`

<br />

> Can be used with other [React Starters](https://appseed.us/apps/react) for a complete **Full-Stack** experience:

| [React Node JS Berry](https://appseed.us/product/berry-dashboard/api-server-nodejs/react/) | [React Node Soft Dashboard](https://appseed.us/product/soft-ui-dashboard/api-server-nodejs/react/) | [React Node Horizon](https://appseed.us/product/horizon-ui/api-server-nodejs/) |
| --- | --- | --- |
| [![React Node JS Berry](https://user-images.githubusercontent.com/51070104/176936514-f1bccb21-bafe-4b43-9e4c-b6fe0ec9511d.png)](https://appseed.us/product/berry-dashboard/api-server-nodejs/react/) | [![React Node Soft Dashboard](https://user-images.githubusercontent.com/51070104/176936814-74386559-4e05-43d5-b9a4-8f70ce96a610.png)](https://appseed.us/product/soft-ui-dashboard/api-server-nodejs/react/) | [![React Node Horizon](https://user-images.githubusercontent.com/51070104/174428337-181e6dea-0ad9-4fe1-a35f-25e5fa656a9d.png)](https://appseed.us/product/horizon-ui/api-server-nodejs/)

<br />

![Flask API Server - Open-source Flask Starter provided by AppSeed.](https://user-images.githubusercontent.com/51070104/126349643-264d4cf4-6d0b-4c24-8185-adf69409fa4e.png)

<br />

## ✨ Quick Start in `Docker`

> Get the code

```bash
$ git clone https://github.com/app-generator/api-server-flask.git
$ cd api-server-flask
```

> Start the app in Docker

```bash
$ docker-compose up --build  
```

The API server will start using the PORT `5000`.

<br />

## ✨ Table of Contents

1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [Modules](#modules)
4. [Testing](#testing)

<br />

## ✨ How to use the code

> **Step #1** - Clone the project

```bash
$ git clone https://github.com/app-generator/api-server-flask.git
$ cd api-server-flask
```

<br />

> **Step #2** - create virtual environment using python3 and activate it (keep it outside our project directory)

```bash
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
```

<br />

> **Step #3** - Install dependencies in virtualenv

```bash
$ pip install -r requirements.txt
```

<br />

> **Step #4** - setup `flask` command for our app

```bash
$ export FLASK_APP=run.py
$ export FLASK_ENV=development
```

 For **Windows-based** systems

```powershell
$ (Windows CMD) set FLASK_APP=run.py
$ (Windows CMD) set FLASK_ENV=development
$
$ (Powershell) $env:FLASK_APP = ".\run.py"
$ (Powershell) $env:FLASK_ENV = "development"
```

<br />

> **Step #5** - start test APIs server at `localhost:5000`

```bash
$ flask run
```

Use the API via `POSTMAN` or Swagger Dashboard.

![Flask API Server - Swagger Dashboard.](https://user-images.githubusercontent.com/51070104/141950891-ea315fca-24c2-4929-841c-38fb950a478d.png) 

<br />

## ✨ Project Structure

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

## ✨ API

For a fast set up, use this `POSTMAN` file: [api_sample](https://github.com/app-generator/api-unified-definition/blob/main/api.postman_collection.json)

> **Register** - `api/users/register` (**POST** request)

```
POST api/users/register
Content-Type: application/json

{
    "username":"test",
    "password":"pass", 
    "email":"test@appseed.us"
}
```

<br />

> **Login** - `api/users/login` (**POST** request)

```
POST /api/users/login
Content-Type: application/json

{
    "password":"pass", 
    "email":"test@appseed.us"
}
```

<br />

> **Logout** - `api/users/logout` (**POST** request)

```
POST api/users/logout
Content-Type: application/json
authorization: JWT_TOKEN (returned by Login request)

{
    "token":"JWT_TOKEN"
}
```

<br />

## ✨ Testing

Run tests using `pytest tests.py`

<br />

---
**Flask API Boilerplate** - provided by AppSeed [App Generator](https://appseed.us)
