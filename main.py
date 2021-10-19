from flask import Flask
from flask import request, render_template
from PersonClass import Person

app = Flask(__name__)


@app.route('/get-person')
def get_person():
    id = request.args.get('id')
    return Person(id).dictify

