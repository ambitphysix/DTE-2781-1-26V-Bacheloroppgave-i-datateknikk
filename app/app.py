from flask import Flask, render_template, redirect, url_for
from flask_wtf.csrf import CSRFProtect
import secrets

application = Flask(__name__)
application.secret_key = secrets.token_urlsafe(32) 
csrf = CSRFProtect(application) 
