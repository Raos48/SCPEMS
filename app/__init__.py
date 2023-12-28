from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
app.static_url_path = 'static'
login_manager = LoginManager()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
babel = Babel(app)
bcrypt = Bcrypt(app)
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Por favor, realize o Login."
login_manager.login_message_category = "info"


from .views import ms_view
from .models import cpems_model
