from flask import render_template, redirect, url_for, flash
from flask_weather import db
from flask_weather.auth import auth_bp
from flask_weather.auth.forms import RegistrationForm
from flask_weather.models import User


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("恭喜，您已成功註冊！", "success")
        return redirect(url_for("main.index"))  # 暫時重導向到首頁，Day 13 補充登入頁面

    return render_template("auth/register.html", title="註冊", form=form)
