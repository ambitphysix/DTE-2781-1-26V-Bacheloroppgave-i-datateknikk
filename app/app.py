from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import config
from cryptography.fernet import Fernet
import secrets
import hashlib


application = Flask(__name__)
application.secret_key = secrets.token_urlsafe(32) 
csrf = CSRFProtect(application) 

# Load the key from file
def load_key():
    with open("key.key", "rb") as key_file:
        return key_file.read()


key = load_key()
fernet = Fernet(key)

# Function to encrypt email
def encrypt_email(email):
    encryped = fernet.encrypt(email.encode()).decode()
    hashed = hashlib.sha256(email.encode()).hexdigest()
    return encryped, hashed


# Function to decrypt email
def decrypt_email(encrypted_email):
    return fernet.decrypt(encrypted_email).decode()

# Function to check email
def check_hashed_email(email):
    return hashlib.sha256(email.encode()).hexdigest()
