from flask import Flask, jsonify, request, session, redirect, url_for
from flask_cors import CORS
from itsdangerous import json
from sqlalchemy import delete, create_engine
from cas import CASClient
from cryptography.fernet import Fernet
import random

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from Class import Class, Student, Assignment, Question, QuestionPart, Param, ParamList, Base

# configuration
DEBUG = True

# TEST KEY, NOT THE REAL KEY, DON'T EVEN TRY IT :)
key = b'SWxUk5xH8mTXngXWpPKGoO7N6ZSzg-2VAlpNuvUKJu4='
f = Fernet(key)

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

cas_client = CASClient(
    version=3,
    service_url='http://localhost:8080/login',
    server_url='https://secure.its.yale.edu/cas/'
)

engine = create_engine('sqlite:///class.db', connect_args = {"check_same_thread": False})

Session = sessionmaker(bind=engine)
sess = Session()

Base.metadata.create_all(engine)

amth_class = sess.query(Class).first()

web_status = ''

if not amth_class:
    amth_class = Class()
    sess.add(amth_class)
    sess.commit()

@app.route('/login/<ticket>', methods=['GET'])
def login(ticket):
    response_object = {'status': 'success'}

    print("Logging in!")

    # There is a ticket, the request come from CAS as callback.
    # need call `verify_ticket()` to validate ticket and get user profile.
    app.logger.debug('ticket: %s', ticket)

    user, attributes, pgtiou = cas_client.verify_ticket(ticket)

    app.logger.debug(
        'CAS verify ticket response: user: %s, attributes: %s, pgtiou: %s', user, attributes, pgtiou)

    if not user:
        response_object['status'] = 'failure'
        response_object['username'] = 'None'
    else:  # Login successfully, redirect according `next` query parameter.
        response_object['username'] = user

    return(jsonify(response_object))

def remove_student(net_id):
    sql = delete(Student).where(Student.net_id == net_id)
    sess.execute(sql)
    sess.commit()
    return False

def remove_assignment(name):
    sql = delete(Assignment).where(Assignment.name == name)
    sess.execute(sql)
    sess.commit()
    return False
    
def remove_question(assign_name, question_name):
    sql = delete(Question).where(Question.name == question_name).where(Question.assignment_name == assign_name)
    sess.execute(sql)
    sess.commit()
    return False

@app.route('/status', methods=['GET', 'PUT'])
def status():
    global web_status
    response_object = {'status': 'success'}
    if request.method == 'GET':
        response_object['status'] = web_status
    if request.method == 'PUT':
        put_data = request.get_json(force=True)
        web_status = put_data.get('status')
    return jsonify(response_object)

@app.route('/manage/student', methods=['GET', 'POST', 'DELETE'])
def modify_student():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json(force=True)
        new_ta = Student(
            post_data.get('net_id'),
            post_data.get('name'),
            is_TA = bool(post_data.get('is_ta'))
        )
        amth_class.students.append(new_ta)
        sess.add(new_ta)
        sess.commit()
        response_object['message'] = 'TA added!'
    if request.method == 'DELETE':
        post_data = request.get_json()
        net_id = post_data.get('net_id')
        remove_student(net_id)
        response_object['message'] = 'Student removed!'
    if request.method == 'GET':
        if request.args.get('get_ta') == 'true':
            response_object['students'] = [s.as_dict() for s in amth_class.get_TAs()]
        else:
            response_object['students'] = [s.as_dict() for s in amth_class.get_enrolled()]
    return jsonify(response_object)

@app.route('/assigns', methods=['GET'])
def all_assign():
    response_object = {'status': 'success'}
    response_object['assignments'] = [a.as_dict() for a in amth_class.assignments]
    return jsonify(response_object)

@app.route('/assign/<assign_name>', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def individual_assign(assign_name=None):
    response_object = {'status': 'success'}
    if request.method == 'POST':
        for a in amth_class.assignments:
            if assign_name == a.name:
                response_object['status'] = 'failure'
                response_object['message'] = 'Assignment already exists!'
                return jsonify(response_object)
        new_assign = Assignment(
            name=assign_name,
        )
        amth_class.assignments.append(new_assign)
        sess.add(new_assign)
        sess.commit()
        response_object['message'] = 'Assignment added!'
    if request.method == 'DELETE':
        remove_assignment(assign_name)
        response_object['message'] = 'Assignment removed!'
    if request.method == 'GET':
        assign = [a for a in amth_class.assignments if a.name == assign_name][0]
        response_object['assignment'] = assign.as_dict()
    if request.method == 'PATCH':
        post_data = request.get_json()
        assign = [a for a in amth_class.assignments if a.name == assign_name][0]
        for param in ('active', 'published'):
            if param in post_data['params']:
                if post_data['params'][param] == True:
                    setattr(assign, param, True)
                elif post_data['params'][param] == False:
                    setattr(assign, param, False)
                else:
                    response_object['status'] = 'failure'
                    response_object['message'] = 'No param status specified'
        sess.commit()
    return jsonify(response_object)

@app.route('/questions/<assign_name>', methods=['GET', 'POST', 'DELETE'])
def get_questions(assign_name=None):
    response_object = {'status': 'success'}
    assign = [a for a in amth_class.assignments if a.name == assign_name][0]
    response_object['questions'] = [q.as_dict() for q in assign.questions]
    return jsonify(response_object)

@app.route('/question/<assign_name>/<question_name>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def question(assign_name=None, question_name=None):
    response_object = {'status': 'success'}
    if request.method == 'GET':
        assign = [a for a in amth_class.assignments if a.name == assign_name][0]
        response_object['question'] = [q.as_dict() for q in assign.questions if q.name==question_name][0]
    else:
        assign = [a for a in amth_class.assignments if a.name == assign_name][0]
        if assign == None:
            response_object['status'] = 'failure'
            return jsonify(response_object)
        if request.method == 'POST':
            new_question = Question(
                name=question_name,
            )
            assign.questions.append(new_question)
            sess.add(new_question)
            sess.commit()
            response_object['message'] = 'Question added!'
        if request.method == 'DELETE':
            remove_question(assign_name, question_name)
            response_object['message'] = 'Assignment removed!'
        if request.method == 'PATCH':
            post_data = request.get_json()
            assign = [a for a in amth_class.assignments if a.name == assign_name][0]
            question = [q for q in assign.questions if q.name==question_name][0]
            for param in ("format", "param_func"):
                if param in post_data['params']:
                    setattr(question, param, post_data['params'][param])
                    if param == 'param_func':
                        add_params(question, post_data['params']['param_func'])
                sess.commit()
            print(question.as_dict())
    return jsonify(response_object)

params = ''
def add_params(question, param_func):
    question.params = []
    for student in amth_class.students:
        p_list = ParamList(student.net_id)
        param_func = "global params\n" + param_func
        exec(param_func)
        for (i, p) in enumerate(params):
            p_list.params.append(Param(i, p))
        question.params.append(p_list)
        print(question.params[0].params)

@app.route('/sampleparamfunc', methods=['PUT'])
def sample_param_func():
    response_object = {'status': 'success', 'param_sample': ''}
    post_data = request.get_json()
    param_func = post_data['params']['param_func']
    param_func = "global params\n" + param_func
    # Scary, I know. Only trusted users can access this endpoint.
    exec(param_func)
    response_object['param_sample'] = params
    return jsonify(response_object)

# Fix the rest of this!
@app.route('/parts', methods=['GET', 'POST', 'DELETE'])
def part():
    response_object = {'status': 'success'}
    if request.method == 'GET':
        post_data = request.args
        assign = None
        for a in amth_class.assignments:
            if post_data.get('assign_name') == a.name:
                assign = a
        # Find the question as well
        print(assign)
        response_object['parts'] = [p.as_dict() for p in assign.questions.question_parts]
        print(response_object)
    else:
        request_data = request.get_json()
        assign = None
        for a in amth_class.assignments:
            if request_data.get('assign_name') == a.name:
                assign = a
        if assign == None:
            response_object['status'] = 'failure'
            return jsonify(response_object)
        if request.method == 'POST':
            post_data = request.get_json(force=True)
            new_question = Question(
                name=post_data.get('question_name'),
            )
            assign.questions.append(new_question)
            print(assign.questions)
            sess.add(new_question)
            sess.commit()
            response_object['message'] = 'Question added!'
        if request.method == 'DELETE':
            post_data = request.get_json()
            remove_question(post_data['assign_name'], post_data['question_name'])
            response_object['message'] = 'Assignment removed!'
    return jsonify(response_object)

if __name__ == '__main__':

    if amth_class.get_TAs() == []:
        head_ta = Student('jtn26', 'Jamie Nachbar', is_TA=True)
        amth_class.students.append(head_ta)
        sess.add(head_ta)
        sess.commit()

    web_status = 'online'

    app.run()
