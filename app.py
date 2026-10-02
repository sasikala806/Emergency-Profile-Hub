from flask import Flask
from flask_cors import CORS
from config import db
from routes.auth_routes import auth_bp
from routes.permission_routes import permission_bp
from routes.qr_routes import qr_bp
app = Flask(__name__)
CORS(app)
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(permission_bp, url_prefix="/api/permissions")
app.register_blueprint(qr_bp, url_prefix="/api/qr")

@app.route("/")
def home():
    return "Emergency Profile Hub Backend is Running!"


@app.route("/test-db")
def test_db():
    try:
        db.command("ping")
        return "MongoDB Connected Successfully!"
    except Exception as e:
        return f"MongoDB Connection Failed: {e}"




if __name__ == "__main__":
    app.run(debug=True)