# Secure Multi-User Task & Notes API

A backend REST API that lets multiple users securely manage their own tasks and notes. Built with FastAPI and SQLAlchemy, focused on proper authentication, data isolation between users, and clean CRUD design.

## Overview

This project was built to strengthen my backend development skills beyond tutorials — implementing real authentication, database relationships, and a properly structured multi-user system rather than a single-user toy app.

## Features

- User registration and login with authentication
- Each user can only access their own tasks and notes (data isolation)
- Full CRUD operations (Create, Read, Update, Delete) for both tasks and notes
- Input validation using Pydantic models
- SQLAlchemy ORM for database interaction

## Tech Stack

- **Language:** Python
- **Framework:** FastAPI
- **Database ORM:** SQLAlchemy
- **Database:** SQLite *(update if different)*
- **Auth:** JWT *(update if different — e.g. OAuth2/session-based)*
- **Validation:** Pydantic

## Project Structure
task-notes-api/
├── main.py
├── models.py
├── schemas.py
├── database.py
├── auth.py
└── requirements.txt

## API Endpoints

| Method | Endpoint          | Description             |
|--------|-------------------|--------------------------|
| POST   | /auth/register    | Register a new user     |
| POST   | /auth/login        | Log in and get access token |
| GET    | /tasks             | Get all tasks for logged-in user |
| POST   | /tasks             | Create a new task       |
| PUT    | /tasks/{id}        | Update a task            |
| DELETE | /tasks/{id}        | Delete a task            |
| GET    | /notes             | Get all notes for logged-in user |
| POST   | /notes             | Create a new note        |
| PUT    | /notes/{id}        | Update a note             |
| DELETE | /notes/{id}        | Delete a note             |

*(this table is a best guess based on your project's purpose — edit it to match your actual routes in main.py)*

## How to Run

```bash
git clone https://github.com/Sanav27/task-notes-api.git
cd task-notes-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Then visit `http://127.0.0.1:8000/docs` for the interactive Swagger API documentation.

## Future Improvements

- Add pagination for large task/note lists
- Add unit tests
- Deploy to a cloud platform

## Author

Sanchit Yadav — [github.com/Sanav27](https://github.com/Sanav27)
