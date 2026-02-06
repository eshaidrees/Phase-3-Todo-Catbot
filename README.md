# Todo Full-Stack Web Application

A full-stack todo application with user accounts, task CRUD operations, and synced database storage.

## Features

- User registration and authentication
- Create, read, update, and delete tasks
- Mark tasks as complete/incomplete
- Responsive UI for desktop and mobile devices
- Secure JWT-based authentication
- Data isolation (users only see their own tasks)

## Tech Stack

### Backend
- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT with secure token handling

### Frontend
- **Framework**: Next.js 16+ (App Router)
- **Styling**: Tailwind CSS
- **HTTP Client**: Built-in fetch API
- **Authentication**: JWT token management

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
   SECRET_KEY=your-super-secret-key-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. Start the backend server:
   ```bash
   python main.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Set up environment variables by creating a `.env.local` file:
   ```
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

The application will be available at `http://localhost:3000`.

## Deployment

### GitHub Integration

1. Initialize git in the project:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Todo Full-Stack Application"
   ```

2. Create a new repository on GitHub and add the remote:
   ```bash
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git branch -M main
   git push -u origin main
   ```

### Backend Deployment (Render)

1. Create an account on [Render](https://render.com)
2. Connect your GitHub repository
3. Create a new Web Service
4. Select your repository
5. Set the environment to "Python"
6. Set the build command: `pip install -r requirements.txt`
7. Set the start command: `uvicorn src.main:app --host=0.0.0.0 --port=$PORT`
8. Add environment variables:
   - `SECRET_KEY`: Your secret key
   - `ALGORITHM`: HS256
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: 30
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `ALLOWED_ORIGINS`: Your frontend URL (e.g., https://your-frontend.vercel.app)
9. Deploy the service

### Frontend Deployment (Vercel)

1. Create an account on [Vercel](https://vercel.com)
2. Connect your GitHub repository
3. Import your project
4. Set the framework preset to "Next.js"
5. Add environment variables:
   - `NEXT_PUBLIC_API_BASE_URL`: Your deployed backend URL (e.g., https://your-backend.onrender.com)
6. Deploy the project

### Alternative: Deploy using Railway

1. Create an account on [Railway](https://railway.app)
2. Connect your GitHub repository
3. Create a new project from your repository
4. Add a PostgreSQL database via the "Provision" menu
5. Add environment variables as needed
6. Deploy the application

### Docker Deployment

The project includes Dockerfiles for both frontend and backend:

1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

This will start both the frontend and backend services with a PostgreSQL database.

## API Endpoints

The application provides the following REST API endpoints:

- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task for a user
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Update task completion status
- `POST /api/register` - Register a new user
- `POST /api/login` - Authenticate a user

## Project Structure

```
backend/
├── src/
│   ├── models/         # Database models (User, Task)
│   ├── services/       # Business logic (auth, task operations)
│   ├── api/            # API routes and dependencies
│   ├── database/       # Database session management
│   └── utils/          # Utility functions
├── tests/              # Test files
├── .env                # Environment variables
├── requirements.txt    # Python dependencies
├── main.py             # Entry point
├── Procfile            # Render deployment configuration
├── runtime.txt         # Python version specification
├── Dockerfile          # Docker configuration
└── render.yaml         # Render deployment manifest

frontend/
├── src/
│   ├── app/            # Next.js App Router pages
│   ├── components/     # React components
│   ├── lib/            # Utilities and API clients
│   └── types/          # Type definitions
├── public/             # Static assets
├── .env.local          # Environment variables
├── package.json        # Node.js dependencies
├── next.config.ts      # Next.js configuration
├── vercel.json         # Vercel deployment configuration
└── Dockerfile          # Docker configuration

├── .gitignore          # Git ignore rules
├── docker-compose.yml  # Docker Compose configuration
├── README.md           # This file
└── prepare-deployment.sh # Deployment preparation script
```

## Security

- JWT tokens are used for authentication and authorization
- Users can only access their own tasks
- Passwords are securely hashed using bcrypt
- Input validation is performed on both frontend and backend
- Environment variables keep sensitive data secure

## Troubleshooting

- If you encounter hydration errors on the dashboard page, make sure your frontend and backend are properly communicating
- Check that your environment variables are correctly set in both development and production
- Verify that your database connection string is properly formatted
- Ensure CORS settings allow requests from your frontend domain

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License.















