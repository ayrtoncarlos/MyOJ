import os
import sys
import filecmp
import re
import subprocess
from subprocess import CalledProcessError, TimeoutExpired, run
from typing_extensions import runtime

STATUS_CODES = {
    200: 'OK',
    201: 'ACCEPTED',
    400: 'WRONG ANSWER',
    401: 'COMPILATION ERROR',
    402: 'RUNTIME ERROR',
    403: 'INVALID FILE',
    404: 'FILE NOT FOUND',
    408: 'TIME LIMIT EXCEEDED'
}

class Program:
    """ Class that handles all the methods of a user program """
    def __init__(self, filename, inputfile, timelimit, expectedOutputFile):
        """ Receives a name of a file from the user. It must be a valid C, C++, Java and Python file """
        self.filename = filename # Full name of the source code file
        self.language = None # Language
        self.name = None # File name without extension
        self.temp = None # File name .class extension
        self.inputfile = inputfile # Input file
        self.timelimit = timelimit # Time limit set for execution in seconds
        self.expectedOutputFile = expectedOutputFile # Expected output file 
        self.actualOutputFile = 'output.txt' # Actual output file
        self.pathTests = '.\\judge\\tests\\'
        self.pathCodes = '.\\judge\\codes\\'
    
    def get_class_name_java(self):
        command = 'dir /s /b "*.class"'
        result = str(subprocess.run(command, stdout=subprocess.PIPE, shell=True).stdout)
        result = result.split('\\')[-3][:-6]
        return result

    def is_valid_file(self):
        """ Checks if the filename is valid """
        validFile = re.compile("^(\S+)\.(java|cpp|c|py)$")
        matches = validFile.match(f'{self.pathCodes}{self.filename}')

        if matches:
            self.name, self.language = matches.groups()
            return True
        return False

    def remove_files(self):
        # Perform cleanup
        if self.language == 'java':
            self.temp = self.get_class_name_java()
            if os.path.isfile(f'{self.pathCodes}{self.temp}.class'):
                os.remove(f'{self.pathCodes}{self.temp}.class')
            if os.path.isfile(f'{self.name}.java'):
                os.remove(f'{self.name}.java')
        elif self.language in ['c', 'cpp']:
            if os.path.isfile(f'{self.name}.exe'):
                os.remove(f'{self.name}.exe')
            if self.language == 'c' and os.path.isfile(f'{self.name}.c'):
                os.remove(f'{self.name}.c')
            else:
                if os.path.isfile(f'{self.name}.cpp'):
                    os.remove(f'{self.name}.cpp')
        elif self.language == 'py' and os.path.isfile(f'{self.name}.py'):
            os.remove(f'{self.name}.py')
    
    def remove_outputfile(self):
        if os.path.isfile(f'{self.pathTests}{self.actualOutputFile}'):
            os.remove(f'{self.pathTests}{self.actualOutputFile}')
    
    def compile(self):
        """ Compiles the given program, returns status code and errors """
        # Remove previous executables
        if os.path.isfile(f'{self.pathCodes}{self.name}'):
            os.remove(f'{self.pathCodes}{self.name}')
        # Check if files are present
        if not os.path.isfile(f'{self.pathCodes}{self.filename}'):
            return 404, 'Missing file'
        
        # Check language
        cmd = None

        if self.language == 'java':
            cmd = f'javac {self.pathCodes}{self.filename}'
        elif self.language == 'c':
            cmd = f'gcc {self.pathCodes}{self.filename} -o {self.name}'
        elif self.language == 'cpp':
            cmd = f'g++ {self.pathCodes}{self.filename} -o {self.name}'
        
        # Invalid files
        if cmd is None:
            self.remove_files()
            return 403, 'File is of invalid type'
        
        try:
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Check for errors
            if proc.returncode != 0:
                self.remove_files()
                return 401, proc.stderr
            else:
                return 200, None
        except CalledProcessError as e:
            self.remove_files()
            print(f'ERROR: {e.output}')
    
    def run(self):
        """ Runs the executable, returns status code and errors """
        # Check if files are present
        if not os.path.isfile(f'{self.pathCodes}{self.filename}'):
            return 404, 'Missing executable file'
        
        # Check language
        cmd = None

        if self.language == 'java':
            self.temp = f'{self.pathCodes} {self.get_class_name_java()}'
            self.temp = replace_nth(self.temp, '\\', ' ', 3)
            cmd = f'java -cp {self.temp}'
        elif self.language in ['c', 'cpp']:
            cmd = self.name
        elif self.language == 'py':
            cmd = f'python {self.pathCodes}{self.filename}'
        
        # Invalid files
        if cmd is None:
            return 403, 'File is of invalid type'
        
        try:
            with open(f'{self.pathTests}output.txt', 'w') as fout:
                fin = None
                if f'{self.pathTests}{self.inputfile}' and os.path.isfile(f'{self.pathTests}{self.inputfile}'):
                    fin = open(f'{self.pathTests}{self.inputfile}', 'r')
                
                proc = subprocess.run(
                    cmd,
                    stdin=fin,
                    stdout=fout,
                    stderr=subprocess.PIPE,
                    timeout=self.timelimit,
                    universal_newlines=True
                )
            
            # Check for errors
            if proc.returncode != 0:
                self.remove_files()
                self.remove_outputfile()
                return 402, proc.stderr
            else:
                self.remove_files()
                return 200, None
        except TimeoutExpired as tle:
            self.remove_files()
            self.remove_outputfile()
            return 408, tle
        except CalledProcessError as e:
            self.remove_files()
            self.remove_outputfile()
            print(f'ERROR: {e.output}')
        
    def match(self):
        """ Compare files to see if they are different, return status code """
        if os.path.isfile(f'{self.pathTests}{self.actualOutputFile}') and os.path.isfile(f'{self.pathTests}{self.expectedOutputFile}'):
            result = filecmp.cmp(f'{self.pathTests}{self.actualOutputFile}', f'{self.pathTests}{self.expectedOutputFile}')

            if result:
                self.remove_outputfile()
                return 201, None
            else:
                self.remove_outputfile()
                return 400, None
        else:
            self.remove_outputfile()
            return 404, 'Missing output files'


def replace_nth(s, sub, repl, n):
    find = s.find(sub)
    # If find is not -1 we have found at least one match for the substring
    i = find != -1
    # loop util we find the nth or we find no match
    while find != -1 and i != n:
        # find + 1 means we start searching from after the last match
        find = s.find(sub, find + 1)
        i += 1
    # If i is equal to n we found nth match so replace
    if i == n:
        return s[:find] + repl + s[find+len(sub):]
    return s

def code_checker(filename, inputfile=None, expectedOutput=None, timeout=1, check=True):
    newProgram = Program(
        filename=filename,
        inputfile=inputfile,
        timelimit=timeout,
        expectedOutputFile=expectedOutput
    )

    status, result = 403, STATUS_CODES[403]

    if newProgram.is_valid_file():
        print('Executing code checker...')
        if not '.py' in filename:
            # Compile program
            compileResult, compileErrors = newProgram.compile()
            status, result = compileResult, STATUS_CODES[compileResult]
            print(f'Compiling ... {STATUS_CODES[compileResult]}({compileResult})', flush=True)
            if compileErrors is not None:
                sys.stdout.flush()
                print(compileErrors, file=sys.stderr)
                return status, result
        
        # Run program
        runtimeResult, runtimeErrors = newProgram.run()
        status, result = runtimeResult, STATUS_CODES[runtimeResult]
        print(f'Running... {STATUS_CODES[runtimeResult]}({runtimeResult})', flush=True)
        if runtimeErrors is not None:
            sys.stdout.flush()
            print(runtimeErrors, file=sys.stderr)
            return status, result
        
        if check:
            # Match expected output
            matchResult, matchErrors = newProgram.match()
            status, result = matchResult, STATUS_CODES[matchResult]
            print(f'Verdict... {STATUS_CODES[matchResult]}({matchResult})', flush=True)
            if matchErrors is not None:
                sys.stdout.flush()
                print(matchErrors, file=sys.stderr)
                return status, result
        return status, result
    else:
        print('FATAL: Invalid file', file=sys.stderr)
        return status, result

'''
if __name__ == '__main__':
    code_checker(
        filename='Subtracao.java',               # Source code file
        inputfile='in_sub.txt',                  # Input file
        expectedOutput='out_sub.txt',     # Expected output
        timeout=1,                              # Time limit
        check=True                              # Set to true to check actual output against expected output
    )
'''