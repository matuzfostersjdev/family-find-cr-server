from flask import Flask
from flask import request, render_template
from PersonClass import Person, PersonList

app = Flask(__name__)


@app.route('/get-person-by-id', methods=['GET'])
def get_person_by_id():
    person_id = request.args.get('id', type=str)
    return Person(person_id).dictify()


@app.route('/get-person-by-name', methods=['GET'])
def get_person_by_name():
    name = request.args.get('name', type=str) if request.args.get('name', type=str) else ''
    surname1 = request.args.get('surname1', type=str) if request.args.get('surname1', type=str) else ''
    surname2 = request.args.get('surname2', type=str) if request.args.get('surname2', type=str) else ''
    return PersonList(name, surname1, surname2).dictify()


@app.route('/get-parents', methods=['GET'])
def get_parents():
    person_id = request.args.get('id', type=str)
    return{
        'father': Person(person_id).get_father().dictify(),
        'mother': Person(person_id).get_mother().dictify()
    }

