from app.schemas import Email, Model, Password


class LoginSchema(Model):
    email: Email
    password: Password


class TokenSchema(Model):
    token: str
    token_type: str


class ForgotPasswordSchema(Model):
    email: Email


class ResetPasswordSchema(Model):
    token: str
    password: Password
