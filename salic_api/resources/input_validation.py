from jsonschema import Draft3Validator
from wtforms import ValidationError

schema = {
    'type': 'object',
    'properties': {
        'PRONAC': {'type': 'number'},
    }
}


def validate_input(input, schema):
    try:
        Draft3Validator(schema).validate(input)
        return True
    except Exception as e:
        return False


def testPRONAC(form, field):
    try:
        int(field.data)
    except ValueError:
        raise ValidationError('PRONAC must be integer')


class InputValidation():
    def __init__(self, fields):
        self.fields = fields

    def validate(self):
        Draft3Validator(schema).validate(self.fields)
