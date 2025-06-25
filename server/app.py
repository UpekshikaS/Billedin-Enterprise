from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

from routes.auth import auth
from routes.invoices import invoices
from routes.stats import stats
from routes.admin import admin

load_dotenv()

app = Flask(__name__)

# CORS setup
CORS(
    app,
    resources={r"/api/*": {"origins": "http://localhost:3000"}},
    supports_credentials=True,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

# JWT setup
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-default-secret')
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(admin)
app.register_blueprint(stats)
app.register_blueprint(invoices)
app.register_blueprint(auth)

@app.route("/")
def home():
    return {"message": "BilledIn Backend is Running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
