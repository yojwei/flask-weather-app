"""
使用者認證路由模組

處理使用者註冊、登入和登出的相關路由和邏輯。
"""

from flask import render_template, redirect, url_for, flash
from flask_weather import db
from flask_weather.auth import auth_bp
from flask_weather.auth.forms import RegistrationForm
from flask_weather.models import User


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    使用者註冊頁面

    GET: 返回註冊表單頁面
    POST: 處理使用者提交的註冊資料
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        # 建立新使用者物件並設定密碼
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        # 將新使用者儲存到資料庫
        db.session.add(user)
        db.session.commit()

        flash("恭喜，您已成功註冊！", "success")
        return redirect(url_for("main.index"))  # 暫時重導向到首頁，Day 13 補充登入頁面

    return render_template("auth/register.html", title="註冊", form=form)
