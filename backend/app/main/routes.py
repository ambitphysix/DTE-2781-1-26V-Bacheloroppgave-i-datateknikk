from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Renders the index page.
    """
    return render_template('index.html')

@main.route('/vis/<side>')
def vis_side(side):
    """
    Renders the visualization page for a specific side.
    """
    return render_template(f'{side}.html')