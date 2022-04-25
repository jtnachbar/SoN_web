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

test_res = ''
@student_api.route('/student/answer/<assign_name>/<question_name>/<part_num>', methods=['GET', 'PATCH'])
def answer(assign_name, question_name, part_num):
    response_object = {'status': 'success'}
    if not check_student_auth(request, response_object):
        return jsonify(response_object)
    sess = current_app.config["session"]
    amth_class = sess.query(Class).first()
    assign_list = [a for a in amth_class.assignments if a.name == assign_name]
    if assign_list == []:
        response_object['status'] = 'failure'
        response_object['message'] = 'No assignment found'
        return jsonify(response_object)
    assign = assign_list[0]
    question_list = [q for q in assign.questions if q.name==question_name]
    if question_list == []:
        response_object['status'] = 'failure'
        response_object['message'] = 'No assignment found'
        return jsonify(response_object)
    question = question_list[0]
    part_list = [p for p in question.question_parts if p.part_num==int(part_num)]
    if part_list == []:
        response_object['status'] = 'failure'
        response_object['message'] = 'No assignment found'
        return jsonify(response_object)
    part = part_list[0]
    student_answer = [ans for ans in part.student_answers if ans.net_id == request.headers['Net_Id']][0]
    if request.method == 'GET':
        response_object['answer'] = student_answer.as_dict()
    elif request.method == 'PATCH':
        # Check to make sure we have a direction
        patch_data = request.get_json()
        if 'answer' not in patch_data:
            response_object['status'] = 'failure'
            response_object['message'] = 'No assignment found'
            return jsonify(response_object)
        student_answer.response = patch_data['answer']
        # evaluate the answer and set 'correct' accordingly
        param_list = [p.params for p in question.params if p.net_id == request.headers['Net_Id']][0]
        param_list = [p.param for p in param_list]
        grading_rule = part.grading_rule
        grading_rule = "global test_res\ntest_res = False\n" + grading_rule
        grading_rule = grading_rule.replace("${s}", patch_data['answer'])
        for (i, val) in enumerate(param_list):
            grading_rule = grading_rule.replace("${" + str(i+1) + "}", val)
        try:
            exec(grading_rule)
            student_answer.correct = test_res
        except:
            student_answer.correct = False
        sess.commit()
    return jsonify(response_object)

@student_api.route('/student/answers/<assign_name>/<question_name>', methods=['GET'])
def get_answer_status(assign_name, question_name):
    response_object = {'status': 'success'}
    if not check_student_auth(request, response_object):
        return jsonify(response_object)
    sess = current_app.config["session"]
    amth_class = sess.query(Class).first()
    assign_list = [a for a in amth_class.assignments if a.name == assign_name]
    if assign_list == []:
        response_object['status'] = 'failure'
        response_object['message'] = 'No assignment found'
        return jsonify(response_object)
    assign = assign_list[0]
    question_list = [q for q in assign.questions if q.name==question_name]
    if question_list == []:
        response_object['status'] = 'failure'
        response_object['message'] = 'No assignment found'
        return jsonify(response_object)
    question = question_list[0]
    response_object['answers'] = {}
    if request.method == 'GET':
        for p in question.question_parts:
            student_answer = [ans for ans in p.student_answers if ans.net_id == request.headers['Net_Id']][0]
            response_object['answers'][p.part_num] = student_answer.correct
    return jsonify(response_object)

@student_api.route('/student/grades', methods=['GET'])
def get_grades():
    response_object = {'status': 'success'}
    if not check_student_auth(request, response_object):
        return jsonify(response_object)
    sess = current_app.config["session"]
    amth_class = sess.query(Class).first()
    grade_dict = {}
    for a in amth_class.assignments:
        grade_dict[a.name] = { 'points': 0, 'total_points': 0, 'questions': {} }
        grade_dict[a.name]['name'] = a.name
        for q in a.questions:
            grade_dict[a.name]['questions'][q.name] = { 'name': q.name, 'parts': {}, 'points': 0, 'total_points': 0 }
            for p in q.question_parts:
                grade_dict[a.name]['questions'][q.name]['parts'][str(p.part_num)] = { 'part_num': p.part_num, 'points': 0 }
                grade_dict[a.name]['questions'][q.name]['parts'][str(p.part_num)]['total'] = p.point_val
                grade_dict[a.name]['questions'][q.name]['total_points'] += p.point_val
                grade_dict[a.name]['total_points'] += p.point_val
                student_answer = [ans for ans in p.student_answers if ans.net_id == request.headers['Net_Id']][0]
                if student_answer.correct:
                    grade_dict[a.name]['questions'][q.name]['parts'][str(p.part_num)]['points'] = p.point_val  
                    grade_dict[a.name]['questions'][q.name]['points'] += p.point_val
                    grade_dict[a.name]['points'] += p.point_val 
                else:
                    grade_dict[a.name]['questions'][q.name]['parts'][str(p.part_num)]['points'] = 0
    response_object['grades'] = grade_dict
    print(grade_dict)
    return jsonify(response_object)
    