
class ParentException(Exception):
     
    information: str

    def __init__(self,message: str):
        super().__init__(message)

    def __str__(self):
       return f'[EXCEPTION]: {self.information}'


class ChildException(ParentException):
    information = 'iam a child exception'

    def __str__(self):
       return f'[EXCEPTION][CHILD]: {self.information}'



try:

    raise ChildException('shit happen')
except ParentException as PE:
    print(PE)

   

