import json 
from pydantic.v1 import BaseModel , error_wrappers 
from .users.schemas import UserSignupSchema
from pydantic.v1.error_wrappers import ValidationError

def valid_schema_or_error(raw_data: dict,SchemaModel: BaseModel):
    errors = []
    data = {}
    error_str = None

    try:
        cleaned_data = SchemaModel(**raw_data)
        data = cleaned_data.dict()  # Only if validation succeeds
        print("Cleaned Data:", data)

    except error_wrappers.ValidationError as e:

        error_str = e.json()
    if error_str is not None:
        try:
            errors = json.loads(error_str)
        except json.JSONDecodeError:
            errors = [{"loc": "non_field_error", "msg": "Unknown error"}]

    print("Errors:", errors)
    return data, errors
    