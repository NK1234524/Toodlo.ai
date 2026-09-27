# Toodlo.ai

A complete AI assisted product for people of various fields so that they could able to make the todolist in their busy schedule. 

Toodlo.ai comprises of proper analysis of priortisation and urgency of the todo task through which the authenticated user can have a good track record of their high priortised of work. This saves the time of the user & make user more focus over the high priority task.

It also provide the user specific daily planning based on the authenticated user's validated data in the todo.The daily planning is not just done through the data of the user present in the Todo list of the database. This gives users a proper task mangement through which they can manage a lot of task seemlessly without any extra manual hurdle & compromise.

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
- AI analysis after the Todo creation through prompt.



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
- Instructions against Ambiguous request
- Instructions given to AI for analysing urgency and priortization of the todo.



## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Check API status |
| POST | `/Toodlo.ai/Register` | Register if new user |
| POST | `/Toodlo.ai/login` | Submit username & Password for Login |
| POST | `/Toodlo.ai/CreateMyTodo` | Create a Todo |
| POST | `/Toodlo.ai/AI/CreateMyTodo` | Create a Todo throguh prompt|
| POST | `/Toodlo.ai/AI/clarifyMyTodo` | Clarify my prompt if it is ambiguous|
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