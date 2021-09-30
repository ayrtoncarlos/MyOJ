from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)

class Problem(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    input_description = db.Column(db.String(1000), nullable=False)
    output_description = db.Column(db.String(1000), nullable=False)
    constraints = db.Column(db.String(100), nullable=False)
    input_examples = db.Column(db.String(1000), nullable=False)
    output_examples = db.Column(db.String(1000), nullable=False)
    time_limit = db.Column(db.Integer, nullable=False)
    input_filename = db.Column(db.String(100), nullable=False)
    output_filename = db.Column(db.String(100), nullable=False)
    accepted = db.Column(db.Integer, nullable=False)
    wrong_answer = db.Column(db.Integer, nullable=False)
    compilation_error = db.Column(db.Integer, nullable=False)
    runtime_error = db.Column(db.Integer, nullable=False)
    time_limit_exceeded = db.Column(db.Integer, nullable=False)

class Result(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'), nullable=False)
    status = db.Column(db.Integer, nullable=False)
