from . import main_bp


@main_bp.route("/")
def index():
    """Home page"""
    return "這是首頁"
