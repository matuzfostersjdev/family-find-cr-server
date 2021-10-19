from flask import Flask
from flask import request, render_template
from PersonClass import Person

app = Flask(__name__)


@app.route('/get-person', methods=['GET'])
def get_person():
    person_id = request.args.get('id', type=str)
    return Person(person_id).dictify()


@app.route('/get-parents', methods=['GET'])
def get_parents():
    person_id = request.args.get('id', type=str)
    return{
        'father': Person(person_id).get_father().dictify(),
        'mother': Person(person_id).get_mother().dictify()
    }

