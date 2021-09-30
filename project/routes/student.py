from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db, create_app

student = Blueprint('student', __name__)

@student.route('/student', methods=['GET'])
@login_required
def student_manager():
    return render_template('student.html', name=current_user.name)
