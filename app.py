from flask import Flask, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import dotenv_values

from app.routes.api import api_bp
from app.routes.bucket import bucket_bp
from app.routes.users import users_bp

from app.extensions import db

app = Flask(__name__, template_folder='app/templates')
config = dotenv_values('.env')
app.config['SQLALCHEMY_DATABASE_URI'] = config['DB_CONNECTION_STRING']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure CORS for '/api' routes
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Configure CORS for '/bucket' routes
CORS(app, resources={r"/bucket/*": {"origins": "http://localhost:3000"}})

# Configure CORS for other routes
CORS(app, resources={r"/*": {"origins": "*"}})

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(bucket_bp, url_prefix='/bucket')
app.register_blueprint(users_bp, url_prefix='/users')

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)