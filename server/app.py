from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from auth import auth
import os
from dotenv import load_dotenv
from routes.invoices import invoices
app.register_blueprint(invoices)
from routes.admin import admin
app.register_blueprint(admin)


load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

app.register_blueprint(auth)

@app.route("/")
def home():
    return {"message": "BilledIn Backend is Running"}

if __name__ == "__main__":
    app.run(debug=True)
