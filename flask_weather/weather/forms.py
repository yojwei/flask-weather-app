from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class SearchForm(FlaskForm):
    city = StringField(
        "City",
        validators=[
            DataRequired(message="請輸入城市名稱"),
            Length(min=2, max=50, message="城市名稱長度需在2到50個字元之間"),
        ],
    )
    submit = SubmitField("搜尋")
