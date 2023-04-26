from config import get_app_config
from models import User, Chore


app_config = get_app_config()
with app_config.app.app.app_context():
    app_config.db.drop_all()
    app_config.db.create_all()
