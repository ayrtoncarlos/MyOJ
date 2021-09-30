from os import stat
import subprocess
import random
import string
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from models.models import Problem
from judge.compiler import code_checker
from app import db, create_app

problem = Blueprint('problem', __name__)


EXTENSIONS_FILE = {
    'python': '.py',
    'java': '.java',
    'c': '.c',
    'cpp': '.cpp'
}

def write_code(code, language):
        
    filename = ''.join(random.choice(string.ascii_lowercase) for _ in range(16)) + EXTENSIONS_FILE[language]
    filePath = f'.\\judge\\codes\\{filename}'

    with open(filePath, 'w+') as fwrite:
        fwrite.write(code)

    return filename

@problem.route('/judge', methods=['POST'])
def compile_code():
    
    print(request.form)
    
    language = request.form.get('language')
    code = request.form.get('code')
    problem_id = request.form.get('problem_id')

    problem = Problem.query.get(problem_id)

    if not problem:
        flash('Problema não encontrado')
        return redirect(f'/problems/{problem_id}')

    filename = write_code(code, language)
    
    status, result = code_checker(filename, problem.input_filename, problem.output_filename, problem.time_limit)

    if result == 'ACCEPTED':
        problem.accepted += 1
    elif result == 'WRONG ANSWER':
        problem.wrong_answer += 1
    elif result == 'COMPILATION ERROR':
        problem.compilation_error += 1
    elif result == 'RUNTIME ERROR':
        problem.runtime_error += 1
    elif result == 'TIME LIMIT EXCEEDED':
        problem.time_limit_exceeded += 1
    
    db.session.commit()

    return jsonify({'result': result})

@problem.route('/problems/<int:id>', methods=["GET"])
def get_problem(id):
    problem = Problem.query.get(id)

    if not problem:
        flash('Problema não encontrado')
        redirect('/problems')
    return render_template('problem.html', title="Problem", problem=problem) 


@problem.route('/problems', methods=['GET'])
def problems_manager():
    count = db.session.query(Problem).count()
    
    if not count:
        flash('Não há problemas cadastrados')
        return render_template('problems.html', title="Counts", count=count)
    
    problems = Problem.query.all()

    return render_template('problems.html', title="Problems", problems=problems, count=count)
