# Toodlo.ai

A RESTful Todo application built with FastAPI backend framework. It is consisting of certain features mentioned below.

## Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- uv
- PostgreSQL
- SQLAlchemy
- psycopg
- ORM(Object Relational Mapping)
- Sessionmaker

## Features

- Create Todo
- Retrieve Todo
- Update Todo
- Delete Todo
- Query Parameters
- Request Validation
- Restrictions & constraints

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Check API status |
| GET | `/Toodlo.ai/login` | Login to Toodlo.ai |
| POST | `/Toodlo.ai/login` | Submit username & Password for Login |
| POST | `/Toodlo.ai/register` | Register if new user |
| GET | `/Toodlo.ai/Home` | Home page |
| POST | `/Toodlo.ai/Home/Todo` | Create a Todo |
| GET | `/Toodlo.ai/Home/Todo` | Get the TODOS |
| PUT | `/Toodlo.ai/Home/Todo/{id}` | Update the Todo in todolist |
| DELETE | `/Toodlo.ai/Home/Todo/{id}` | Delete the Todo in todolist |



## Project Structure

```text
Toodlo.ai/src/toodlo_ai
 ├── main.py
 ├── database.py
 ├── models.py
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore