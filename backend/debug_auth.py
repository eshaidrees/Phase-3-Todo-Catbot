#!/usr/bin/env python3
"""Debug script to test the authentication functionality"""

import sys
import os
import traceback

# Add the backend src to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sqlmodel import Session, select
from src.database.session import get_session, engine
from src.models.user import User, UserCreate
from src.services.auth import AuthService

def test_database_connection():
    print("Testing database connection...")
    try:
        # Create tables first
        from src.database.session import create_db_and_tables
        create_db_and_tables()
        print("[INFO] Tables created successfully")

        # Test basic connection
        with Session(engine) as session:
            print("[SUCCESS] Database connection successful")

            # Test if tables exist by trying to query
            existing_users = session.exec(select(User)).all()
            print(f"[SUCCESS] Table query successful. Found {len(existing_users)} users")

            return True
    except Exception as e:
        print(f"[ERROR] Database connection failed: {str(e)}")
        traceback.print_exc()
        return False

def test_user_creation():
    print("\nTesting user creation...")
    try:
        # Create a test user
        user_create = UserCreate(
            email="debug_test@example.com",
            password="testpass123",
            name="Debug Test User"
            # is_verified is optional, default is False
        )

        with Session(engine) as session:
            # Check if user already exists
            existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
            if existing_user:
                print("User already exists, skipping creation")
                return True

            # Hash the password
            hashed_password = AuthService.get_password_hash(user_create.password)

            # Create the user object - notice that we're not setting id explicitly since it should auto-generate
            db_user = User(
                email=user_create.email,
                name=user_create.name,
                hashed_password=hashed_password
                # id will be auto-generated, is_verified defaults to False
            )

            print(f"Creating user with ID: {getattr(db_user, 'id', 'NO_ID_SET')}")

            # Add to session and commit
            session.add(db_user)
            session.commit()
            session.refresh(db_user)

            print(f"[SUCCESS] User created successfully with ID: {db_user.id}")
            return True

    except Exception as e:
        print(f"[ERROR] User creation failed: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting authentication debug...")

    if test_database_connection():
        test_user_creation()

    print("\nDebug complete.")