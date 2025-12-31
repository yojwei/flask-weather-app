"""
使用者認證路由模組

處理使用者註冊、登入和登出的相關路由和邏輯。
"""

from functools import wraps
from flask import render_template, redirect, url_for, flash, request
from flask_weather import db
from flask_weather.auth import auth_bp
from flask_weather.auth.forms import RegistrationForm, LoginForm
from flask_weather.models import User
from flask_login import current_user, login_user, logout_user, login_required


def redirect_if_authenticated(f):
    """
    裝飾器：若使用者已登入，重導向到首頁

    應用於登入和註冊路由，防止已登入使用者重複登入。
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)

    return decorated_function


@auth_bp.route("/register", methods=["GET", "POST"])
@redirect_if_authenticated
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


@auth_bp.route("/login", methods=["GET", "POST"])
@redirect_if_authenticated
def login():
    """
    使用者登入頁面

    GET: 返回登入表單頁面
    POST: 驗證使用者憑證並登入
    """
    form = LoginForm()
    if form.validate_on_submit():
        # 根據使用者名稱查詢使用者
        user = User.query.filter_by(username=form.username.data).first()

        # 驗證使用者是否存在且密碼正確
        if user is None or not user.check_password(form.password.data):
            flash("使用者名稱或密碼錯誤。", "danger")
            return redirect(url_for("auth.login"))

        # 登入使用者（支援記住我功能）
        login_user(user, remember=form.remember_me.data)

        # 重導向到原始頁面，若無則導向首頁
        next_page = request.args.get("next")
        if not next_page or not next_page.startswith("/"):
            next_page = url_for("main.index")

        return redirect(next_page)

    return render_template("auth/login.html", title="登入", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    """
    使用者登出

    登出目前登入的使用者並重導向到首頁。
    需要使用者已登入（由 @login_required 裝飾器保護）。
    """
    logout_user()
    return redirect(url_for("main.index"))
