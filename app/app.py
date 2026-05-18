from flask import Flask
from flask_wtf.csrf import CSRFProtect
import secrets

application = Flask(__name__)
application.secret_key = secrets.token_urlsafe(32) 
csrf = CSRFProtect(application) 
