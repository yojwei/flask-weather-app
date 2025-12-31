from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from flask_weather.models import User


class RegistrationForm(FlaskForm):
    username = StringField("使用者名稱", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "密碼",
        validators=[DataRequired(), Length(min=6, message="密碼必須至少6個字元")],
    )
    confirm_password = PasswordField(
        "確認密碼",
        validators=[DataRequired(), EqualTo("password", message="密碼必須相符")],
    )
    submit = SubmitField("註冊")

    # 自定義驗證：檢查使用者名稱是否已存在
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("此使用者名稱已被使用。")

    # 自定義驗證：檢查 Email 是否已存在
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("此 Email 已被註冊。")


class LoginForm(FlaskForm):
    username = StringField("使用者名稱", validators=[DataRequired()])
    password = PasswordField("密碼", validators=[DataRequired()])
    remember_me = BooleanField("記住我")
    submit = SubmitField("登入")
