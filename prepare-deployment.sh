#!/bin/bash
# Deployment preparation script

echo "Preparing Todo Full-Stack Application for Deployment..."

# Backend setup
echo "Setting up backend..."
cd backend
if [ ! -f ".env" ]; then
    echo "Creating .env file for backend..."
    cp .env.example .env.example.bak 2>/dev/null || echo "No .env.example found"

    # Create a sample .env for production
    cat > .env.production << EOF
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql://postgres:password@localhost:5432/todo_db
ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
ENVIRONMENT=production
EOF
fi

# Frontend setup
echo "Setting up frontend..."
cd ../frontend
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file for frontend..."
    cat > .env.local << EOF
NEXT_PUBLIC_API_BASE_URL=https://your-backend-url.onrender.com
EOF
fi

echo "Deployment preparation completed!"
echo ""
echo "Next steps:"
echo "1. Update the environment variables with your actual values"
echo "2. Push the code to GitHub: git add . && git commit -m 'Prepare for deployment' && git push origin main"
echo "3. Deploy the backend to Render/Railway/Fly.io"
echo "4. Deploy the frontend to Vercel"
echo "5. Update environment variables on deployment platforms"