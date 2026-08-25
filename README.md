# Toodlo.ai

A RESTful Todo application built with FastAPI, developed while learning and exploring backend development.

## Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- uv

## Features

- Create Todo
- Retrieve Todo
- Update Todo
- Delete Todo
- Query Parameters
- Request Validation

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Check API status |
| GET | `/todos` | Retrieve todos |
| POST | `/todos` | Create a todo |
| PUT | `/todos/{id}` | Update a todo |
| DELETE | `/todos/{id}` | Delete a todo |

## Project Structure

```text
Toodlo.ai/
├── main.py
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore