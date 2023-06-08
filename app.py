from flask import Flask, render_template
from flask_cors import CORS
from dotenv import dotenv_values
from flask_login import LoginManager

from app.routes.api import api_bp
from app.routes.bucket import bucket_bp
from app.routes.users import users_bp
from app.routes.auth import auth_bp
from app.routes.json import json_bp

from app.extensions import db

from app.models.user import User

app = Flask(__name__, template_folder='app/templates')
config = dotenv_values('.env')
app.config['SQLALCHEMY_DATABASE_URI'] = config['DB_CONNECTION_STRING']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = config['SECRET_KEY']

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(bucket_bp, url_prefix='/bucket')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(json_bp, url_prefix='/json')

# Configure CORS for '/api' routes
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000", "supports_credentials": True}})

# Configure CORS for '/bucket' routes
CORS(app, resources={r"/bucket/*": {"origins": "http://localhost:3000", "supports_credentials": True}})

# Configure CORS for '/users' routes
CORS(app, resources={r"/users/*": {"origins": "http://localhost:3000", "supports_credentials": True}})

# Configure CORS for '/auth' routes
CORS(app, resources={r"/auth/*": {"origins": "http://localhost:3000", "supports_credentials": True}})

# Configure CORS for '/auth' routes
CORS(app, resources={r"/json/*": {"origins": "http://localhost:3000", "supports_credentials": True}})

# Configure CORS for other routes
CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})

login_manager = LoginManager(app)
login_manager.session_protection = "strong"
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # Load the user object from the database based on the user_id
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, use_reloader=True)