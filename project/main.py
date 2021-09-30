from flask_login import login_required, current_user
from flask import Blueprint, render_template
from models.models import Problem
from app import db, create_app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile', methods=['GET'])
@login_required
def profile():
    problems = Problem.query.all()
    return render_template('profile.html', name=current_user.name, title='Problems', problems=problems)

if __name__ == '__main__':
    app = create_app()
    app.run()
