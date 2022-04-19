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

def remove_part(question_name, part_num):
    sql = delete(QuestionPart).where(QuestionPart.question_name == question_name).where(QuestionPart.part_num == part_num)
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
def get_assigns():
    response_object = {'status': 'success'}
    response_object['assignments'] = [a.as_dict() for a in amth_class.assignments]
    return jsonify(response_object)

@app.route('/assign/<assign_name>', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def assign(assign_name=None):
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
            print('failed a')
            return jsonify(response_object)
        if request.method == 'POST':
            for a in amth_class.assignments:
                for q in a.questions:
                    if q.name == question_name:
                        response_object['status'] = 'failure'
                        response_object['message'] = 'Question already exists!'
                        return jsonify(response_object)
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
            patch_data = request.get_json()
            assign = [a for a in amth_class.assignments if a.name == assign_name][0]
            question = [q for q in assign.questions if q.name==question_name][0]
            for param in ("format", "param_func"):
                if param in patch_data:
                    setattr(question, param, patch_data[param])
                    if param == 'param_func':
                        add_params(question, patch_data['param_func'])
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
        question.param_num = len(p_list.params)
        print(question.params[0].params)

@app.route('/sampleparamfunc', methods=['PUT'])
def sample_param_func():
    response_object = {'status': 'success', 'param_sample': ''}
    put_data = request.get_json()
    param_func = put_data['param_func']
    param_func = "global params\n" + param_func
    # Scary, I know. Only trusted users can access this endpoint.
    exec(param_func)
    response_object['param_sample'] = params
    return jsonify(response_object)

test_res = ''
@app.route('/samplegradingrule', methods=['PUT'])
def sample_grading_rule():
    response_object = {'status': 'success', 'test_res': ''}
    put_data = request.get_json()
    grading_rule = put_data['grading_rule']
    grading_rule = "global test_res\ntest_res = False\n" + grading_rule
    grading_rule = grading_rule.replace("${s}", put_data['test_ans'])
    for (i, val) in enumerate(put_data['params']):
        grading_rule = grading_rule.replace("${" + str(i+1) + "}", val)
    # Scary, I know. Only trusted users can access this endpoint.
    exec(grading_rule)
    print(test_res)
    response_object['test_res'] = str(test_res)
    return jsonify(response_object)

@app.route('/parts/<assign_name>/<question_name>', methods=['GET'])
def get_parts(assign_name, question_name):
    response_object = {'status': 'success'}
    assign = [a for a in amth_class.assignments if a.name == assign_name][0]
    question = [q for q in assign.questions if q.name==question_name][0]
    question.question_parts.sort(key=lambda x: x.part_num)
    response_object['parts'] = [p.as_dict() for p in question.question_parts]
    return jsonify(response_object)

@app.route('/part/<assign_name>/<question_name>/<part_num>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def part(assign_name, question_name, part_num):
    response_object = {'status': 'success'}
    assign = [a for a in amth_class.assignments if a.name == assign_name][0]
    if assign == None:
        response_object['status'] = 'failure'
        return jsonify(response_object)
    question = [q for q in assign.questions if q.name==question_name][0]
    if question == None:
        response_object['status'] = 'failure'
        return jsonify(response_object)
    if request.method == 'GET':
        response_object['part'] = [p.as_dict() for p in question.question_parts if p.part_num == int(part_num)][0]
    elif request.method == 'POST':
        new_part = QuestionPart()
        # Give it the last number by default
        if question.question_parts == []:
            largest_num = 1
        else:
            largest_num = max([int(p.part_num) for p in question.question_parts]) + 1
        new_part.part_num = largest_num
        question.question_parts.append(new_part)
        sess.add(new_part)
        sess.commit()
        response_object['message'] = 'Part added!'
    elif request.method == 'DELETE':
        remove_part(question_name, part_num)
        for part in question.question_parts:
            if part.part_num > int(part_num):
                part.part_num -= 1
        response_object['message'] = 'Part removed!'
    elif request.method == 'PATCH':
        patch_data = request.get_json()
        part = [p for p in question.question_parts if p.part_num == int(part_num)][0]
        if part == None:
            response_object['status'] = 'failure'
            return jsonify(response_object)
        if 'part_order' in patch_data:
            new_pos = int(patch_data['part_order'])
            if part.part_num < new_pos:
                for p in question.question_parts:
                    if p.part_num > part.part_num and p.part_num <= new_pos:
                        p.part_num -= 1
            else:
                for p in question.question_parts:
                    if p.part_num < part.part_num and p.part_num >= new_pos:
                        p.part_num += 1
            part.part_num = new_pos
        if 'directions' in patch_data:
            part.direction = patch_data['directions']
        if 'grading_rule' in patch_data:
            part.grading_rule = patch_data['grading_rule']
        sess.commit()

    return jsonify(response_object)

if __name__ == '__main__':

    if amth_class.get_TAs() == []:
        head_ta = Student('jtn26', 'Jamie Nachbar', is_TA=True)
        amth_class.students.append(head_ta)
        sess.add(head_ta)
        sess.commit()

    web_status = 'online'

    app.run()
