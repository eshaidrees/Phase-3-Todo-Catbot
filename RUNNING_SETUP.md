# Running Setup Guide

This document explains how to properly set up and run the Todo Catbot application after fixing the authentication issues.

## Fixed Issues

### 1. Frontend API Configuration
- **Problem**: Frontend was configured to connect to a remote Hugging Face Space URL instead of the local backend
- **Solution**: Updated `frontend/.env.local` to point to the correct local backend URL (`http://localhost:7860`)

### 2. Backend Server Not Running
- **Problem**: The backend server was not running, so authentication endpoints were inaccessible
- **Solution**: Installed dependencies and started the backend server

## How to Run the Application

### Prerequisites
- Python 3.8+
- Node.js 18+

### Backend Setup (Port 7860)

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
python -c "from src.main import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=7860)"
```
Or alternatively:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 7860
```

The backend server will be accessible at `http://localhost:7860`

### Frontend Setup (Port 3000)

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be accessible at `http://localhost:3000`

### API Endpoints

- Root: `http://localhost:7860/`
- Login: `POST http://localhost:7860/api/login`
- Register: `POST http://localhost:7860/api/register`
- User Tasks: `GET/POST/PUT/DELETE http://localhost:7860/api/{user_id}/tasks`

### Authentication Flow

1. Users can register at `/signup` on the frontend
2. Users can login at `/login` on the frontend
3. Upon successful authentication, JWT tokens are stored in localStorage
4. Authenticated users are redirected to the dashboard
5. Protected routes verify the JWT token with each request

## Troubleshooting

### Common Issues:

1. **Frontend can't connect to backend**:
   - Verify backend server is running on port 7860
   - Check that `frontend/.env.local` contains `NEXT_PUBLIC_API_BASE_URL=http://localhost:7860`

2. **Backend won't start**:
   - Ensure all dependencies from `requirements.txt` are installed
   - Check that the `.env` file in the backend directory has the required environment variables

3. **Database connection errors**:
   - Verify your `DATABASE_URL` in the backend `.env` file
   - The application uses Neon PostgreSQL by default, but can be changed to local SQLite for development

## Environment Variables

### Frontend (frontend/.env.local):
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:7860
```

### Backend (backend/.env):
```
DATABASE_URL=postgresql://neondb_owner:npg_LmMwTn1l4xfe@ep-cold-feather-ahn19pv6-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
SECRET_KEY=supersecretkeythatshouldbechangedinproduction
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```