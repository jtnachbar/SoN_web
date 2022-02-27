from urllib import response
from xmlrpc.client import Boolean
from flask import Flask, jsonify, request, session, redirect, url_for
from flask_cors import CORS
from itsdangerous import json
from sqlalchemy import delete, create_engine, Column, Integer, String, Boolean
from cas import CASClient


from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# configuration
DEBUG = True

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


def remove_book(book_id):
    sql = delete(Books).where(Books.id == book_id)
    sess.execute(sql)
    sess.commit()
    return False

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        new_book = Books(
            title = post_data.get('title'),
            author = post_data.get('author'),
            read = post_data.get('read')
        )
        sess.add(new_book)
        sess.commit()
        response_object['message'] = 'Book added!'
    else:
        books = sess.query(Books).all()
        response_object['books'] = [book.as_dict() for book in books]
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        new_book = Books(
            title = post_data.get('title'),
            author = post_data.get('author'),
            read = post_data.get('read')
        )
        sess.add(new_book)
        sess.commit()
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)

Base = declarative_base()

class Books(Base):
    __tablename__ = 'Books'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    read = Column(Boolean)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'Title: {self.title}'

if __name__ == '__main__':
    engine = create_engine('sqlite:///books.db', echo=True, connect_args = {"check_same_thread": False})

    Session = sessionmaker(bind=engine)
    sess = Session()

    Base.metadata.create_all(engine)

    sess.commit()

    app.run()
