from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class Class(Base):
    __tablename__ = 'class'

    id = Column(Integer, primary_key=True)
    # The net_id of the head TA / Webmaster
    head_net_id = Column(String)
    assignments = relationship('Assignment')
    students = relationship('Student')

    def __init__(self):
        self.assignments = []
        self.students = []

    def get_TAs(self):
        res = []
        for s in self.students:
            if s.is_TA:
                res.append(s)
        return res

class Student(Base):
    __tablename__ = 'student'

    net_id = Column(String, primary_key=True)
    name = Column(String)
    # The authentication token (hashed based on net_id)
    token = Column(String)
    class_id = Column(Integer, ForeignKey('class.id'))
    is_TA = Column(Boolean)

    def __init__(self, net_id, name, is_TA=False):
        self.net_id = net_id
        self.name = name
        self.is_TA = is_TA

    def __str__(self):
        return self.net_id

class Assignment(Base):
    __tablename__ = 'assignment'

    id = Column(Integer, primary_key=True)
    html = Column(String)
    class_id = Column(Integer, ForeignKey('class.id'))
    questions = relationship('Question')

    def __init__(self, html, questions):
        self.html = html
        self.questions = questions

class Question(Base):
    __tablename__ = 'question'

    net_id = Column(String, primary_key=True)
    params = relationship('Param')
    answers = relationship('Answer')
    assignment_id = Column(Integer, ForeignKey('assignment.id'))

    def __init__(self, net_id, param_list, answer_list):
        self.net_id = net_id
        self.params = param_list
        self.answers = answer_list

class Answer(Base):
    __tablename__ = 'answer'

    id = Column(Integer, primary_key=True)
    response = Column(String)
    answer = Column(String)
    grading_rule = Column(String)
    net_id = Column(Integer, ForeignKey('question.net_id'))

    def __init__(self, res, ans):
        self.response = res
        self.answer = ans

class Param(Base):
    __tablename__ = 'param'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    param = Column(String)
    net_id = Column(Integer, ForeignKey('question.net_id'))

    def __init__(self, name, param):
        self.name = name
        self.param = param
