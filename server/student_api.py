from flask import Blueprint, jsonify, current_app, request

from Class import Class, Student, Assignment, Question, QuestionPart, Param, ParamList, Base

student_api = Blueprint('student_api', __name__)

# To do:

def check_student_auth(request, response_object):
    if 'Authorization' not in request.headers or 'Net_Id' not in request.headers:
        response_object['status'] = 'failure'
        return False
    else:
        sess = current_app.config["session"]
        amth_class = sess.query(Class).first()
        s_list = [s for s in amth_class.students if s.net_id == request.headers['Net_Id']]
        if s_list == None:
            response_object['status'] = 'failure'
            return False
        else:
            student = s_list[0]
            if request.headers['Authorization'] != student.token:
                print(request.headers['Authorization'])
                print(student.token)
                response_object['status'] = 'failure'
                return False
    return True

def format_question(q, net_id):
    param_list = [param_list for param_list in q.params if param_list.net_id == net_id][0]
    modified_format = q.format
    for i, p in enumerate(param_list.params):
        modified_format = modified_format.replace("${" + str(i+1) + "}", p.param)
    return {'name': q.name, 'format': modified_format}

@student_api.route('/student/assigns', methods=['GET'])
def get_assigns():
    response_object = {'status': 'success'}
    if not check_student_auth(request, response_object):
        return jsonify(response_object)
    sess = current_app.config["session"]
    amth_class = sess.query(Class).first()
    res_list = [a.as_dict() for a in amth_class.assignments if a.published]
    for d in res_list:
        del d['published']
    response_object['assignments'] = res_list
    return jsonify(response_object)

# Change the format before sending it over
@student_api.route('/student/questions/<assign_name>/<net_id>', methods=['GET'])
def get_questions(assign_name=None, net_id=None):
    response_object = {'status': 'success'}
    if not check_student_auth(request, response_object):
        return jsonify(response_object)
    sess = current_app.config["session"]
    amth_class = sess.query(Class).first()
    assign = [a for a in amth_class.assignments if a.name == assign_name][0]
    if assign == None:
        response_object['status'] = 'failure'
        response_object['message'] = 'No assignment found'
        return jsonify(response_object)
    res_list = [format_question(q, net_id) for q in assign.questions]
    response_object['questions'] = res_list
    return jsonify(response_object)

@student_api.route('/student/parts/<assign_name>/<question_name>', methods=['GET'])
def get_parts(assign_name, question_name):
    response_object = {'status': 'success'}
    if not check_student_auth(request, response_object):
        return jsonify(response_object)
    sess = current_app.config["session"]
    amth_class = sess.query(Class).first()
    assign = [a for a in amth_class.assignments if a.name == assign_name][0]
    question = [q for q in assign.questions if q.name==question_name][0]
    question.question_parts.sort(key=lambda x: x.part_num)
    response_object['parts'] = [p.as_dict() for p in question.question_parts]
    return jsonify(response_object)