from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask('__name__', template_folder='sik/templates', static_folder='sik/static')
app.config['SECRET_KEY'] = "vividaaaa"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sik.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from sik.routes import vmahasiswa
app.register_blueprint(vmahasiswa)
