from flask import Blueprint, jsonify, current_app, request

from Class import Class, Student, Assignment, Question, QuestionPart, Param, ParamList, Base

student_api = Blueprint('student_api', __name__)

# To do:
# Change format before sending over question list
# When we click a dropdown, set current stuff based on the array we already got

@student_api.route('/student/assigns', methods=['GET'])
def get_assigns():
    sess = current_app.config["session"]
    amth_class = sess.query(Class).first()
    response_object = {'status': 'success'}
    res_list = [a.as_dict() for a in amth_class.assignments]
    for d in res_list:
        del d['published']
    response_object['assignments'] = res_list
    return jsonify(response_object)

# Change the format before sending it over
@student_api.route('/student/questions/<assign_name>', methods=['GET'])
def get_questions(assign_name=None):
    response_object = {'status': 'success'}
    sess = current_app.config["session"]
    amth_class = sess.query(Class).first()
    assign = [a for a in amth_class.assignments if a.name == assign_name][0]
    if assign == None:
        response_object['status'] = 'failure'
        response_object['message'] = 'No assignment found'
        return jsonify(response_object)
    res_list = [q.as_dict() for q in assign.questions]
    for d in res_list:
        del d['param_func']
    response_object['questions'] = res_list
    return jsonify(response_object)

@student_api.route('/student/parts/<assign_name>/<question_name>', methods=['GET'])
def get_parts(assign_name, question_name):
    sess = current_app.config["session"]
    amth_class = sess.query(Class).first()
    response_object = {'status': 'success'}
    assign = [a for a in amth_class.assignments if a.name == assign_name][0]
    question = [q for q in assign.questions if q.name==question_name][0]
    question.question_parts.sort(key=lambda x: x.part_num)
    response_object['parts'] = [p.as_dict() for p in question.question_parts]
    return jsonify(response_object)