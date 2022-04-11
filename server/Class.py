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

    def get_enrolled(self):
        res = []
        for s in self.students:
            if not s.is_TA:
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

    def as_dict(self):
        return {'net_id': self.net_id, 'name': self.name}

    def __str__(self):
        return self.net_id + ": " + self.name

class Assignment(Base):
    __tablename__ = 'assignment'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    class_id = Column(Integer, ForeignKey('class.id'))
    questions = relationship('Question')
    published = Column(Boolean)
    active = Column(Boolean)

    def __init__(self, name):
        self.questions = []
        self.name = name
        self.published = False
        self.active = False

    def as_dict(self):
        return {'name': self.name, 'published': self.published, 'active': self.active}

class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    params = relationship('ParamList')
    format = Column(String)
    assignment_name = Column(Integer, ForeignKey('assignment.name'))
    question_parts = relationship('QuestionPart')

    def __init__(self, name):
        self.name = name
        self.format = ''

    def as_dict(self):
        return {'name': self.name, 'format': self.format}

class QuestionPart(Base):
    __tablename__ = 'question_part'

    id = Column(Integer, primary_key=True)
    part_num = Column(Integer)
    direction = Column(String)
    grading_rule = Column(String)
    question_id = Column(Integer, ForeignKey('question.id'))
    student_answers = relationship('StudentAnswer')

    def __init__(self, direction):
        self.direction = direction

    def as_dict(self):
        return {'part_num': self.part_num}

class StudentAnswer(Base):
    __tablename__ = 'student_answer'
    
    id = Column(Integer, primary_key=True)
    net_id = Column(String)
    response = Column(String)
    correct = Column(Boolean)
    question_part_id = Column(Integer, ForeignKey('question_part.id'))

    def __init__(self, net_id):
        self.net_id = net_id

class ParamList(Base):
    __tablename__ = 'param_list'
    
    id = Column(Integer, primary_key=True)
    net_id = Column(String)
    params = relationship('Param')
    question_id = Column(Integer, ForeignKey('question.id'))

class Param(Base):
    __tablename__ = 'param'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    param = Column(String)
    param_list_id = Column(Integer, ForeignKey('param_list.id'))

    def __init__(self, name, param):
        self.name = name
        self.param = param
