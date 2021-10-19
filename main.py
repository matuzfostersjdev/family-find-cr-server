from flask import Flask
from flask import request, render_template
from PersonClass import Person

app = Flask(__name__)


@app.route('/get-person', methods=['GET'])
def get_person():
    person_id = request.args.get('id', type=str)
    return Person(person_id).dictify

