from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import timedelta
from src.database.session import get_session
from src.services.auth import AuthService
from src.models.user import User, UserCreate, UserRead
from typing import Dict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get token expiration from environment
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

router = APIRouter()

@router.post("/register", response_model=dict)
def register(user: UserCreate, session: Session = Depends(get_session)):
    # Check if user already exists
    from sqlmodel import select
    existing_user_statement = select(User).where(User.email == user.email)
    existing_user = session.exec(existing_user_statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    try:
        # Create new user
        db_user = AuthService.create_user(session, user)

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthService.create_access_token(
            data={"sub": db_user.email, "user_id": str(db_user.id)},
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        # Log the error for debugging
        import traceback
        print(f"Error in register: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login")
def login(user_credentials: Dict[str, str], session: Session = Depends(get_session)):
    email = user_credentials.get("email")
    password = user_credentials.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password required"
        )

    # Try to authenticate user
    user = AuthService.authenticate_user(session, email=email, password=password)

    # Check if user was not found in the database
    if user is None:
        # The authenticate_user function already handles the different cases
        # and logs appropriate debug messages
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is not verified (if verification is required)
    if not user.is_verified:
        # Optionally, you can return a different error for unverified users
        # For now, we'll allow unverified users to login but you can uncomment the following:
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="Account not verified. Please verify your email.",
        #     headers={"WWW-Authenticate": "Bearer"},
        # )

        # For now, just print a warning and continue with login
        print(f"WARNING: Unverified user {email} is logging in")

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": user.email, "user_id": str(user.id)},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}