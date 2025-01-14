import json
from colorama import Fore, Back, Style
from typing_extensions import Literal


class Logging:

    @staticmethod
    def success(msg: str,void=True) -> None:
        if void:
            print(f'{Fore.GREEN}{msg}{Style.RESET_ALL}')
        return f'{Fore.GREEN}{msg}{Style.RESET_ALL}'

    @staticmethod
    def error(msg: str,void=True) -> None:
        if void:
            print(f'{Fore.RED}{msg}{Style.RESET_ALL}')
        return f'{Fore.RED}{msg}{Style.RESET_ALL}'

    @staticmethod
    def warning(msg: str,void=True) -> None:
        if void:
            print(f'{Fore.YELLOW}{msg}{Style.RESET_ALL}')
        return f'{Fore.YELLOW}{msg}{Style.RESET_ALL}'

    @staticmethod
    def info(msg: str,void=True) -> None:
        if void:
            print(f'{Fore.BLUE}{msg}{Style.RESET_ALL}')
        return f'{Fore.BLUE}{msg}{Style.RESET_ALL}'



class InvalidDataException(Exception):

    invalid_type: str

    def __init__(self,message: str,fieldType: Literal['username','password','semester','nilai_evaluasi_dosen']):
        super().__init__(message)
        self.type_field = fieldType 
        self.message = message

    def __str__(self):
        return Logging.error(f'[{self.invalid_type}][{self.type_field}]: {self.message}')


class BlankData(InvalidDataException):
    invalid_type = 'EMPTY FIELD' 


class EvalDosenValueOutOfRange(InvalidDataException):
    invalid_type = 'OUT OF RANGE 1 - 4' 


class InvalidProcessException(Exception):
    
    process_stage: str

    def __init__(self,message: str):
        super().__init__(message)
        self.message = message


    def __str__(self):
        return Logging.error(f'[{self.process_stage}][ERROR]: {self.message}')


class InvalidLoginProcess(InvalidProcessException):
    process_stage = 'LOGIN'


class InvalidMoveToKHSPage(InvalidProcessException):
    process_stage = 'MOVE TO KHS PAGE'


class InvalidSelectSemesterAndShowingKhs(InvalidProcessException):
    process_stage = 'SHOWING KHS DATA'

class InvalidFillDosenEvaluation(InvalidProcessException):
    process_stage = 'FILL THE EVAL DOSEN'






class Data:

    def init_data(self,source_data: str):
        with open(source_data,'r') as json_file:
            data = json.load(json_file)      
            self.username = data.get('username','')
            self.password = data.get('password','')
            self.semester = data.get('semester','')
            self.nilai_evaluasi_dosen = int(data.get('nilai_evaluasi_dosen',-1)) 

    # memvalidasi apakah semua informasi telah sesuai 
    def validate_information(self):
        if self.username == '':
            raise BlankData('username tidak boleh kosong','username')

        if self.password == '':
            raise BlankData('password tidak boleh kosong','password')

        if self.semester == '':
            raise BlankData('semester tidak boleh kosong','semester')

        if self.nilai_evaluasi_dosen < 1:
            raise EvalDosenValueOutOfRange('nilai tidak valid','nilai_evaluasi_dosen')


