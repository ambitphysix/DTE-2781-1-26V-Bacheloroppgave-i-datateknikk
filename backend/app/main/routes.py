from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Renders the index page.
    """
    return render_template('index.html')