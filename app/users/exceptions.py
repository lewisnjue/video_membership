
from fastapi import HTTPException

class UserAlreadyExistsException(Exception):
      """
      user already has account
      """
      pass 


class InvalidEmailException(Exception):
      """
        email is invalid 

      """
      pass


class UserIdException(Exception):
     """
     user id exception
     """
     


class LoginRequiredException(HTTPException):

    """ 
    class LoginRequiredException(Exception):
    pass  """

    pass 

