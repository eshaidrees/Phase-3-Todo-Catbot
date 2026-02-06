# Quickstart Guide: Todo Full-Stack Web Application

## Prerequisites

- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- PostgreSQL-compatible database (Neon Serverless recommended)
- Git
- Package managers: pip (Python) and npm/yarn (Node.js)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup

#### Navigate to Backend Directory
```bash
cd backend
```

#### Create Virtual Environment and Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Environment Configuration
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
NEON_DATABASE_URL=your-neon-database-url
```

#### Run Database Migrations
```bash
# Initialize the database and run migrations
python -m src.database.migrate
```

#### Start the Backend Server
```bash
uvicorn src.main:app --reload --port 8000
```

### 3. Frontend Setup

#### Navigate to Frontend Directory
```bash
cd frontend  # from project root
```

#### Install Dependencies
```bash
npm install
# or
yarn install
```

#### Environment Configuration
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXTAUTH_SECRET=your-nextauth-secret
NEXTAUTH_URL=http://localhost:3000
```

#### Start the Development Server
```bash
npm run dev
# or
yarn dev
```

## Development Workflow

### Backend Development
1. Activate virtual environment: `source venv/bin/activate`
2. Make changes to backend code
3. Server auto-reloads on file changes (when running with `--reload`)

### Frontend Development
1. Run `npm run dev` to start the development server
2. Make changes to frontend code
3. Browser auto-refreshes on file changes

## API Interaction

The frontend communicates with the backend via the API endpoints defined in the contract:
- Authentication handled by Better Auth
- Task operations via `/api/{user_id}/tasks` endpoints
- JWT tokens automatically attached to requests

## Database Migrations

When you make changes to the data models:
1. Update the model definitions in `src/models/`
2. Create a new migration: `alembic revision --autogenerate -m "Description of changes"`
3. Apply the migration: `alembic upgrade head`

## Running Tests

### Backend Tests
```bash
# Run all backend tests
pytest

# Run with coverage
pytest --cov=src
```

### Frontend Tests
```bash
# Run all frontend tests
npm run test

# Run tests in watch mode
npm run test:watch
```

## Deployment

### Backend Deployment
1. Ensure environment variables are set appropriately for the target environment
2. Build and deploy the Python application
3. Run database migrations in the target environment

### Frontend Deployment
1. Build the application: `npm run build`
2. Serve the build output through a web server

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in the startup commands
2. **Database connection errors**: Verify DATABASE_URL in environment variables
3. **Authentication issues**: Ensure Better Auth is properly configured
4. **CORS errors**: Check backend CORS settings during development

### Resetting Development Data
To reset your development database:
```bash
# In backend directory
python -m src.database.reset
```