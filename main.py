from flask import Flask
from flask import request, render_template
from PersonClass import Person

app = Flask(__name__)


@app.route('/get-person', methods=['GET'])
def get_person():
    person_id = request.args.get('id', type=str)
    print(person_id)
    return Person(person_id).dictify()  # Fix 3 arguments being passed

