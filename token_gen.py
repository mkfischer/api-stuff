#!/usr/bin/env python

from cryptography.fernet import Fernet
import base64
import os

# Dictionary of API versions and their respective bit lengths
API_VERSIONS = {"1.01": 28, "1.2": 32, "1.3": 56, "1.4": 64}


# Obscure the salt by encoding it
def obscure_salt(salt):
    return base64.urlsafe_b64encode(salt.encode("utf-8"))


# Generate a Fernet key from the salt
def generate_fernet_key(salt):
    obscured_salt = obscure_salt(salt)
    # Ensure the key length is 32 bytes (256 bits) for Fernet
    return base64.urlsafe_b64encode(obscured_salt.ljust(32, b"\0"))


# Generate a reversible token
def generate_token(api_version, fernet_key):
    fernet = Fernet(fernet_key)
    # Generate a random token of the specified bit length
    token_length = API_VERSIONS[api_version] // 8  # Convert bits to bytes
    token = os.urandom(token_length)
    # Encrypt the token to make it reversible
    encrypted_token = fernet.encrypt(token)
    return encrypted_token


# Main function to generate tokens and write to file
def main():
    # Obscured salt (VESTAS!123)
    salt = "VESTAS!123"[::-1]  # Simple reversal to obscure the salt
    fernet_key = generate_fernet_key(salt)

    with open("good_tokens.txt", "w") as file:
        for api_version in API_VERSIONS:
            file.write(f"API Version: {api_version}\n")
            for x in range(10):
                token = generate_token(api_version, fernet_key)
                file.write(f"{token.decode()}\n")


if __name__ == "__main__":
    main()
