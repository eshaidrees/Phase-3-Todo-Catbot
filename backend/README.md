# Todo API Backend

A FastAPI backend for the Todo application with user authentication and task management.

## Features

- User registration and authentication with JWT
- CRUD operations for tasks
- Secure password hashing with bcrypt
- PostgreSQL database with SQLModel ORM
- CORS support for frontend integration
- Full API documentation available

## Endpoints

- `POST /api/register` - Register a new user
- `POST /api/login` - Login and get JWT token
- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Mark task as complete/incomplete

## API Documentation

Documentation is available at:
- `/docs` - Interactive Swagger UI
- `/redoc` - ReDoc documentation

## Deployment to Hugging Face Spaces

This backend is configured to run on Hugging Face Spaces.

### Requirements for Hugging Face Spaces:

1. **Dockerfile** - Included in the repository
2. **requirements.txt** - Python dependencies
3. **Environment Variables** (set in Hugging Face Spaces settings):
   - `DATABASE_URL` - Database connection string (defaults to local SQLite if not provided)

### To deploy to Hugging Face Spaces:

1. Create a new Space on Hugging Face
2. Choose "Docker" as the SDK
3. Point to this repository
4. Add any required environment variables
5. The application will automatically deploy and be accessible at `https://your-username.hf.space`

### Port Configuration

The application is configured to run on port 7860, which is the standard port for Hugging Face Spaces.

## Local Development

To run locally:

```bash
pip install -r requirements.txt
python main.py
```

The server will start on `http://localhost:7860`

## Environment Variables

- `DATABASE_URL` - Database connection string (optional, defaults to local SQLite)
- `SECRET_KEY` - Secret key for JWT tokens (optional, generates random if not provided)
- `ALGORITHM` - Hash algorithm for JWT (defaults to HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time (defaults to 30 minutes)
- `ALLOWED_ORIGINS` - Comma-separated list of allowed origins for CORS (defaults to localhost)

## Database

The application uses SQLModel with SQLAlchemy to interact with the database. On first run, it will automatically create the necessary tables.

## Contributing

Feel free to submit issues and enhancement requests!