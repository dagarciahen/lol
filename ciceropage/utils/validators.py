from wtforms.validators import ValidationError


class Unique(object):
    def __init__(self, model, field, message="This element already exists."):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field, *args, **kwargs):
        exists = self.model.query.filter(self.field == field.data).first()
        if exists:
            raise ValidationError(self.message, *args, **kwargs)
