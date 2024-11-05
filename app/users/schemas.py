from pydantic.v1 import (BaseModel,
                         EmailStr,
                         SecretStr,
                         validator,
                         root_validator
                         )
from . import auth

from .models import User


class UserSignupSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    password_confirm: SecretStr

    @validator('email')
    def email_available(cls,v,values,**kwargs):
        q = User.objects.filter(email=v)
        if q.count() != 0:
            raise ValueError("email not available")
        else:
            return v            

    @validator('password_confirm')
    def password_match(cls, v, values):
        if 'password' in values:
            if v != values['password']:
                raise ValueError('Passwords do not match')
        return v

    def __init__(self, **data):
        super().__init__(**data)
        if self.password != self.password_confirm:
            raise ValueError('Passwords do not match')
    

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    token: str = None

    @root_validator
    def validate_user(cls, values):
        err_msg = "Incorrect credentials, please try again"
        email = values.get('email')
        password = values.get('password')

        if email is None or password is None:
            raise ValueError(err_msg)

        password = password.get_secret_value()
        user_obj = auth.authenticate(email, password)
        if user_obj is None:
            raise ValueError(err_msg)
        token = auth.login(user_obj, expires=100)
        values['session_id'] = token
        return values


