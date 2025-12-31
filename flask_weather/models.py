from datetime import datetime
from flask_weather import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """User model to store user information"""

    __tablename__ = "users"  # table name in the database

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 關聯關係
    saved_cities = db.relationship(
        "SavedCity", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    search_histories = db.relationship(
        "SearchHistory", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class SavedCity(db.Model):
    __tablename__ = "saved_cities"

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # 外鍵關聯
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SavedCity {self.city_name}>"


class SearchHistory(db.Model):
    __tablename__ = "search_history"

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    searched_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 避免重複記錄：同一用戶對同一城市的搜尋
    __table_args__ = (
        db.UniqueConstraint("user_id", "city_name", name="unique_user_city_search"),
    )

    def __repr__(self):
        return f"<SearchHistory {self.city_name} by {self.user.username}>"


# User Loader for Flask-Login
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
