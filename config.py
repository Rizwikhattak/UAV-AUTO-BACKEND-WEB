from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# root / Admin@1234  →  Admin%401234
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://root:Admin%401234@localhost:3306/uavauto"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Initialize Flask-Migrate
# migrate = Migrate(app, db)

# Import models to ensure they are registered
# from Model.User import User
# from Model.Operator import Operator


# $env:FLASK_APP = "main.py"


# flask db init   # Run only if 'migrations' folder doesn't exist
# flask db migrate -m "Initial migration"
# flask db upgrade
