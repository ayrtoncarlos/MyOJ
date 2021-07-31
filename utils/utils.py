import os
import subprocess

def remove_file(directory, filename):
    path = directory
    dir = os.listdir(path)
    for file in dir:
        if file == filename:
            os.remove(file)

def teste_script(command):

    output = None

    try:
        output = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        output = e.output

    if output == b'':
        print('Executado com sucesso.')
    else:
        print('Erro ao executar.')

def getResultado(command_compare):

    out_1 = b'N\xc6o \x82 poss\xa1vel localizar/abrir o arquivo'
    out_2 = b'Os arquivos possuem tamanhos diferentes'
    out_3 = b'Compara\x87\xc6o de arquivos correta'
    output = None

    try:
        output = subprocess.check_output(command_compare, shell=True)
    except subprocess.CalledProcessError as e:
        output = e.output

    print()
    print('OUTPUT:', output)
    if out_1 in output:
        print('Pelo menos 1 dos arquivos não foi encontrado.')
        return '2'
    elif out_2 in output:
        print('Os arquivos possuem tamanhos diferentes.')
        return '1'
    elif out_3 in output:
        print('Os arquivos são iguais.')
        return '0'
    else:
        print('Erro desconhecido.')
        return '-1'

def salvarResultado(numero_problema, arq_saida_1, arq_saida_2, resultado):
    with open('resultados.txt', 'a+') as arq:
        arq.write(numero_problema + ";")
        arq.write(arq_saida_1 + ";")
        arq.write(arq_saida_2 + ";")
        arq.write(resultado)
        arq.write('\n')
		
def get_script(filename, author, number_problem):
    parts = filename.split('_')
    if parts[0] == number_problem and parts[1] == author:
        script = filename.split('.')
        if script[1] == 'py': return True
        else: return False

def get_tests(filename, author, number_problem):
    parts = filename.split('_')
    if parts[0] == number_problem and parts[1] == author:
        script = filename.split('.')
        if script[1] == 'txt': return True
        else: return False

def execute(number_problem, script_aluno):

    script_professor = ""
    txt = ""
    folder = "uploads"

    for dirname, _, filenames in os.walk(f'./{folder}/'):
        for filename in filenames:
            if get_script(filename, "professor", number_problem): script_professor = filename
            elif get_tests(filename, "professor", number_problem): txt = filename
    '''
    for dirname, _, filenames in os.walk(f'./{folder}/'):
        for filename in filenames:
            if get_script(filename, "aluno", number_problem): script_aluno = filename
    '''
    command_professor = ['python', f'../{folder}/{script_professor}', '<', f'../{folder}/{txt}', '>', f'{number_problem}_professor_out_1.txt']
    command_aluno = ['python', f'../{folder}/{script_aluno}', '<', f'../{folder}/{txt}', '>', f'{number_problem}_aluno_out_2.txt']
    
    teste_script(command_professor)
    teste_script(command_aluno)

    command_compare = ['echo', 'N', '|', 'comp', f'{number_problem}_professor_out_1.txt', f'{number_problem}_aluno_out_2.txt', '/d', '/a', '/l']

    salvarResultado(number_problem, script_professor, script_aluno, getResultado(command_compare))

    #current_directory = os.path.dirname(os.path.realpath(__file__))
    #remove_file(current_directory, f'{number_problem}_professor_out_1.txt')
    #remove_file(current_directory, f'{number_problem}_aluno_out_2.txt')
