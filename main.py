import os
import urllib.request
from utils import utils
from pathlib import Path
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'py'])

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def salvarResultado(numero_problema, arq_saida_1, arq_saida_2, resultado):
	with open('resultados.txt', 'a+') as arq:
		arq.write(numero_problema + ";")
		arq.write(arq_saida_1 + ";")
		arq.write(arq_saida_2 + ";")
		arq.write(getResultado(arq_saida_1, arq_saida_2))
		arq.write('\n')

def getResultado(arq_saida_1, arq_saida_2):
	
	command_compare = f"echo N | comp {arq_saida_1} {arq_saida_2} /d /a /l"
	
	print(os.system(command_compare))
	
	if os.system(command_compare) == 0:
		print("Os arquivos são iguais")
		return 1
	elif os.system(command_compare) == 2:
		print("Pelo menos 1 dos arquivos não foi encontrado")
		return 0
	else:
		print("Os arquivos são diferentes")
		return 0

def gerarArquivosDeSaida():
	return None

def getNumeroDoProblema(flag):

	caminho = Path('./resultados.txt')

	if isFileExists(caminho):
		print('Arquivo existe!')
		with open(caminho, 'r') as f:
			n_linhas = len(f.readlines())
		print('Ele tem {} linhas.'.format(n_linhas))
		if flag: return str(n_linhas)
		flash(f'Problema {n_linhas+1} adicionado!')
	else:
		print('Arquivo inexistente :(')
		if flag: return '1'
		flash('Problema 1 adicionado!')

def isFileExists(path):
	return os.path.isfile(path)

@app.route('/problemas')
def problemas():
	return render_template('problemas.html')

@app.route('/professor')
def professor():
    return render_template('professor.html')

@app.route('/aluno')
def aluno():
    return render_template('aluno.html')

@app.route('/aluno', methods=['POST'])
def upload_file_aluno():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('Sem parte do arquivo')
			return redirect(request.url)

		number = request.form['number']
		file = request.files['file']

		if file.filename == '':
			flash('Nenhum arquivo selecionado para envio')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(number) + '_aluno_' + filename))
			flash('Arquivo enviado com sucesso')
			utils.execute(number, str(number) + '_aluno_' + filename)
			return redirect('/aluno')
		else:
			flash('Os tipos de arquivo permitidos são txt e py')
			return redirect(request.url)

@app.route('/professor', methods=['POST'])
def upload_file_professor():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('Sem parte do arquivo')
			return redirect(request.url)

		titulo = request.form['titulo']
		descricao = request.form['descricao']
		entrada = request.form['entrada']
		saida = request.form['saida']
		exemplos_entrada = request.form.getlist('exemplo_entrada')
		exemplos_saida = request.form.getlist('exemplo_saida')
		tle = request.form['tle']
		upload_files = request.files.getlist("file")
		count_files = 0

		exemplos = []

		for x, y in zip(exemplos_entrada, exemplos_saida):
			exemplos.append([x, y])

		print(titulo)
		print(descricao)
		print(entrada)
		print(saida)
		print(exemplos)
		print(tle)
		print(upload_files)
		
		for file in upload_files:
			if file.filename == '':
				flash('Nenhum arquivo selecionado para envio')
				return redirect(request.url)
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				numero_problema = getNumeroDoProblema(True)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], numero_problema + '_professor_' + filename))
				if count_files == 1:
					flash('Arquivos enviados com sucesso')
					getNumeroDoProblema(False)
					return redirect('/professor')
				else:
					count_files += 1
			else:
				flash('Os tipos de arquivo permitidos são txt e py')
				return redirect(request.url)
    
@app.route('/')
def main():
    return render_template('index.html'), 200

if __name__ == '__main__':
    app.run(debug=True)