# Toodlo.ai
An AI powered SAAS project

A complete AI assisted Todo app for people of various fields so that they could able to make the todolist in their busy schedule. 

Toodlo.ai comprises of proper analysis of priortisation and urgency of the todo task through which the authenticated user can have a good track record of their high priortised of work. This saves the time of the user & make user more focus over the high priority task.

It also provide the user specific daily planning based on the authenticated user's validated data in the todo.The daily planning is not just done through the data of the user present in the Todo list of the database. This gives users a proper task mangement through which they can manage a lot of task seemlessly without any extra manual hurdle & compromise.

Adaptive replanning feature is something very significant feature in this app. This will help the user's to remove that cumbersome process of replanning the todo's task daily manually. AI(Gemini) will on their own handle all the todo's daily planning in such a way so that the user will get the todo's in the daily plan of the very next in their particular timezone inclusive of that tasks also which are not having  completed status in the last day Daily planning. This will make the  daily planning of everyday well replanned and able to make the user's cumbersome work so light.



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
- Instructions against Ambiguous request
- Instructions given to AI for analysing urgency and priortization of the todo.
- Daily planning of User's todos
- Adaptive replanning of tasks by Gemini


## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Check API status |
| POST | `/Toodlo.ai/Register` | Register if new user |
| POST | `/Toodlo.ai/login` | Submit username & Password for Login |
| POST | `/Toodlo.ai/CreateMyTodo` | Create a Todo |
| POST | `/Toodlo.ai/AI/CreateMyTodo` | Create a Todo throguh prompt|
| POST | `/Toodlo.ai/AI/clarifyMyTodo` | Clarify my prompt if it is ambiguous|
| POST | `/Toodlo.ai/AI/DailyPlan` | Create a Daily plan for the authenticated user's data|
| POST | `/Toodlo.ai/AI/Adaptive Replanning` | Adaptive Replanning of tasks |
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
                                        ├── Daily_Planning_instruction.py
                        ├──client.py
                        ├──deadline.py
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