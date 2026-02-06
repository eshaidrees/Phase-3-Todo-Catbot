#!/usr/bin/env python3
"""Test the new password hashing context with argon2"""

from passlib.context import CryptContext

# New password hashing context with argon2 as primary
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

password = "testpass123"
print(f"Password: '{password}'")
print(f"Password length: {len(password)} characters")
print(f"Password byte length: {len(password.encode('utf-8'))} bytes")

try:
    hashed = pwd_context.hash(password)
    print(f"Hash successful with scheme: {pwd_context.identify(hashed)}")
    print(f"Hash: {hashed[:50]}...")

    # Verify the hash
    verified = pwd_context.verify(password, hashed)
    print(f"Verification successful: {verified}")
except Exception as e:
    print(f"Hash failed: {e}")
    import traceback
    traceback.print_exc()

# Test with another password
password2 = "another_test_password"
print(f"\nSecond password: '{password2}'")
try:
    hashed2 = pwd_context.hash(password2)
    print(f"Second hash successful: {hashed2[:50]}...")

    # Verify the second hash
    verified2 = pwd_context.verify(password2, hashed2)
    print(f"Second verification successful: {verified2}")
except Exception as e:
    print(f"Second hash failed: {e}")
    import traceback
    traceback.print_exc()