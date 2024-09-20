from marshmallow import Schema, fields, validates, ValidationError
import re  

class RegisterSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @validates('username')
    def validate_username(self, value):
        if len(value) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        if not value.isalnum():
            raise ValidationError("Username must contain only alphanumeric characters.")

    @validates('email')
    def validate_email(self, value):
        if "@" not in value or "." not in value:
            raise ValidationError("Invalid email format.")

    @validates('password')
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", value):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", value):
            raise ValidationError("Password must contain at least one number.")
        if not re.search(r"[@$!%*?&]", value):
            raise ValidationError("Password must contain at least one special character (@, $, !, %, *, ?, &).")
