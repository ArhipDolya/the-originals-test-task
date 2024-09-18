# Task Management System

This project is a Task Management System built with FastAPI and SQLAlchemy.

## Features

- Create, edit, and delete tasks
- Assign tasks to users
- Set task priority and status
- Role-based access control
- Email notifications for task status changes (mock implementation)

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/ArhipDolya/the-originals-test-task.git
   ```

2. Create a `.env` file in the root directory and add the following environment variables:
   ```
    # Postgres
    POSTGRES_DB=your_database_name
    POSTGRES_USER=your_username
    POSTGRES_PASSWORD=your_password
    POSTGRES_HOST=postgresql
    POSTGRES_PORT=5432

    # JWT
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

3. Build and run the Docker containers:
   ```
   docker compose up --build
   ```

4. The API will be available at `http://localhost:8000`

5. Access the API documentation at `http://localhost:8000/api/docs`

## Apply Database Migrations

In a new terminal window, apply the database migrations using Alembic:
```
    docker compose exec backend alembic upgrade head
```
This will create the necessary tables in your PostgreSQL database.
