from flask import Flask, render_template
from flask_cors import CORS
from app.routes.api import api_bp
from app.routes.bucket import bucket_bp

app = Flask(__name__, template_folder='app/templates')

# Configure CORS for '/api' routes
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Configure CORS for '/bucket' routes
CORS(app, resources={r"/bucket/*": {"origins": "http://localhost:3000"}})

# Configure CORS for other routes
CORS(app, resources={r"/*": {"origins": "*"}})

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(bucket_bp, url_prefix='/bucket')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)