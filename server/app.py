from flask import Flask, jsonify, request, session, redirect, url_for
from flask_cors import CORS
from itsdangerous import json
from sqlalchemy import delete, create_engine, Column, Integer, String, Boolean
from cas import CASClient
from cryptography.fernet import Fernet

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from Class import Class, Student, Assignment, Question, Answer, Param, Base

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

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

#@app.route('/books', methods=['GET', 'POST'])
#def all_books():
#    response_object = {'status': 'success'}
#    if request.method == 'POST':
#        post_data = request.get_json()
#        new_book = Books(
#            title = post_data.get('title'),
#            author = post_data.get('author'),
#            read = post_data.get('read')
#        )
#        sess.add(new_book)
#        sess.commit()
#        response_object['message'] = 'Book added!'
#    else:
#        books = sess.query(Books).all()
#        response_object['books'] = [book.as_dict() for book in books]
#    return jsonify(response_object)


@app.route('/manage/student', methods=['GET', 'PUT', 'DELETE'])
def modify_student():
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json(force=True)
        new_ta = Student(
            net_id = post_data.get('net_id'),
            name = post_data.get('name'),
            is_ta = bool(post_data.get('is_ta'))
        )
        amth_class.students.append(Student)
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

if __name__ == '__main__':

    if amth_class.get_TAs() == []:
        head_ta = Student('jtn26', 'Jamie Nachbar', is_TA=True)
        amth_class.students.append(head_ta)
        sess.add(head_ta)
        sess.commit()

    app.run()
