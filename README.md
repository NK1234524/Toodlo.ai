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
- psycopg (DBAPI driver / network driver)
- ORM(Object Relational Mapping)
- Sessionmaker
- Authentication & Authorization
- AI agent
- Gemini API key



## Features

- Create Todo
- Retrieve Todo
- Update Todo
- Delete Todo
- Query Parameters
- Request Validation
- Restrictions & constraints
- Hashing (pwdlib (Argon2 + parameters) pwd_hash)
- verification (pwdlib (Argon2 + parameters) pwd_verify)
- OAuth2
- OAuthpasswordReceiver
- AI integration with authentication
- PostgreSQL DB connection with Gemini api 
- Automatic data creation in DB



## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Check API status |
| POST | `/Toodlo.ai/Register` | Register if new user |
| POST | `/Toodlo.ai/login` | Submit username & Password for Login |
| POST | `/Toodlo.ai/CreateMyTodo` | Create a Todo |
| GET | `/Toodlo.ai/GetMyTodos` | Get the TODOS of user |
| PUT | `/Toodlo.ai/UpdateMyTodos/{id}` | Update the Todo in todolist |
| DELETE | `/Toodlo.ai/DeleteMyTodo/{id}` | Delete the Todo in todolist |



## Project Structure

```text
Toodlo.ai/
    ├── src/
        ├── toodlo_ai
                    ├── main.py
                    ├── AI/
                        ├── Instruction/
                                        ├── todo_creation.py
                        client.py
                    ├── Db/
                        ├── database.py
                        ├── models.py
                    ├── Auth/
                        ├── security_key.py
                    ├── Schemas/
                        ├── schema.py
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore