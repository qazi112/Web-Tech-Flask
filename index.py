from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return '<a href="/"><h1>Go to Index</h1></a>'


@app.route('/user/<user_id>')
def user(user_id):
    breakpoint()
    return f'User Id is{user_id}'



if __name__ == '__main__':
   app.run(debug = True)