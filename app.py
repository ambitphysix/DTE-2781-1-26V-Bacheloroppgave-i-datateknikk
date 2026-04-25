from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/map')
def map():
    return render_template('map.html')

# Login er foreløpig ikke implementert
@app.route('/login')
def login():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
