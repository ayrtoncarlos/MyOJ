import os
from pathlib import Path
from flask_login import login_required, current_user
from flask import Blueprint, current_app, render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
from models.models import Problem
from app import db, create_app


professor = Blueprint('professor', __name__)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS'] 

def is_file_exists(path):
	return os.path.isfile(path)

@professor.route('/professor', methods=['GET', 'POST'])
@login_required
def professor_manager():
    if request.method == 'POST': 
        if 'file' not in request.files:
            flash('Sem parte do arquivo')
            return redirect(request.url)

        count = db.session.query(Problem).count()
        last_id = 0

        if count == 0:
            last_id = 1
        else:
            last_id = db.session.query(Problem).order_by(Problem.id.desc()).first().id + 1
    
        title = request.form.get('title')
        description = request.form.get('description')
        input_description = request.form.get('input_description')
        output_description = request.form.get('output_description')
        constraints = request.form.get('constraints')
        input_examples = request.form.getlist('input_examples')
        output_examples = request.form.getlist('output_examples')
        time_limit = request.form.get('time_limit')
        upload_files = request.files.getlist('file')
        input_filename = f'{last_id}_{upload_files[0].filename}'
        output_filename = f'{last_id}_{upload_files[1].filename}'
        count_files = 0
        
        examples = []
        
        for x, y in zip(input_examples, output_examples):
            examples.append([x, y])
        
        print(title)
        print(description)
        print(input_description)
        print(output_description)
        print(constraints)
        print(examples)
        print(time_limit)
        print(input_filename)
        print(output_filename)
        print(upload_files)

        problem = Problem.query.filter_by(title=title).first()

        if problem:
            flash('Já existe um problema com esse título')
            return redirect(request.url)

        input_examples = ' '.join([str(x) for x in input_examples])
        output_examples = ' '.join([str(x) for x in output_examples])
        time_limit = int(time_limit)

        new_problem = Problem(title=title, description=description, input_description=input_description, 
            output_description=output_description, constraints=constraints , input_examples=input_examples, output_examples=output_examples, 
            time_limit=time_limit, input_filename=input_filename, output_filename=output_filename, accepted=0,
            wrong_answer=0, compilation_error=0, runtime_error=0, time_limit_exceeded=0)
                
        db.session.add(new_problem)
        db.session.commit()

        problem_id = Problem.query.filter_by(title=title).first().id
        
        for file in upload_files:
            filename = ''

            if file.filename == '':
                flash('Nenhum arquivo selecionado para envio')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                if not os.path.isdir(current_app.config['UPLOAD_FOLDER']):
                    os.mkdir(current_app.config['UPLOAD_FOLDER'])

                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], f'{problem_id}_{filename}'))
                
                if count_files == 1:
                    flash('Arquivos enviados com sucesso')
                    return redirect(request.url)
                else:
                    count_files += 1
                
            else:
                flash('Os tipos de arquivo permitidos são .txt')
                return redirect(request.url)
            
    return render_template('professor.html', name=current_user.name)
