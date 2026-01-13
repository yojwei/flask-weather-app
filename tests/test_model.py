from flask_weather.models import User


def test_password_hashing():
    u = User(username="susan")
    u.set_password("cat")

    assert u.check_password("cat")
    assert not u.check_password("dog")


def test_user_representation():
    u = User(username="john")
    assert repr(u) == "<User john>"
