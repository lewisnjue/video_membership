from pydantic.v1 import BaseModel,EmailStr,SecretStr,validator


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
    