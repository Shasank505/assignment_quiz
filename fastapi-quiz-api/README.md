# FastAPI Quiz API

This project is a role-based quiz API built with FastAPI and integrated with a PostgreSQL database. It supports user authentication and role management for Admin and Participant users.

## Features

- User registration and login
- Role management (Admin and Participant)
- CRUD operations for quizzes and questions
- Secure JWT authentication
- Pydantic schemas for data validation

## Technologies Used

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic for database migrations
- Pydantic for data validation

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd fastapi-quiz-api
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up the PostgreSQL database:**
   - Create a new database in PostgreSQL.
   - Update the database connection settings in `app/core/config.py`.

5. **Run database migrations:**
   ```
   alembic upgrade head
   ```

6. **Start the FastAPI application:**
   ```
   uvicorn app.main:app --reload
   ```

## API Endpoints

- **Authentication:**
  - `POST /register`: Register a new user
  - `POST /login`: Authenticate a user

- **Quizzes:**
  - `POST /quizzes`: Create a new quiz (Admin only)
  - `PUT /quizzes/{quiz_id}`: Update an existing quiz (Admin only)
  - `DELETE /quizzes/{quiz_id}`: Delete a quiz (Admin only)

- **Users:**
  - `GET /users`: Retrieve user information (Admin only)

## Testing

To run the tests, use the following command:
```
pytest app/tests
```

## License

This project is licensed under the MIT License.