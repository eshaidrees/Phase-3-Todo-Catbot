@echo off
REM Deployment preparation script for Windows

echo Preparing Todo Full-Stack Application for Deployment...

REM Backend setup
echo Setting up backend...
cd backend
if not exist ".env" (
    echo Creating .env file for backend...
    REM Create a sample .env for production
    echo SECRET_KEY=your-super-secret-key-change-in-production>> .env
    echo ALGORITHM=HS256>> .env
    echo ACCESS_TOKEN_EXPIRE_MINUTES=30>> .env
    echo DATABASE_URL=postgresql://postgres:password@localhost:5432/todo_db>> .env
    echo ALLOWED_ORIGINS=https://your-frontend-url.vercel.app>> .env
    echo ENVIRONMENT=production>> .env
)

REM Frontend setup
echo Setting up frontend...
cd ..\frontend
if not exist ".env.local" (
    echo Creating .env.local file for frontend...
    echo NEXT_PUBLIC_API_BASE_URL=https://your-backend-url.onrender.com>> .env.local
)

echo Deployment preparation completed!
echo.
echo Next steps:
echo 1. Update the environment variables with your actual values
echo 2. Push the code to GitHub: git add . && git commit -m "Prepare for deployment" && git push origin main
echo 3. Deploy the backend to Render/Railway/Fly.io
echo 4. Deploy the frontend to Vercel
echo 5. Update environment variables on deployment platforms