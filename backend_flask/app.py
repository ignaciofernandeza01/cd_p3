from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from db import Base, engine
from routes_auth import bp_auth
from routes_games import bp_games
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET", "cambia-esto")
    JWTManager(app)

    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_games)

    @app.get("/")
    def health():
        return jsonify({"status": "ok"})
    return app

app = create_app()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    app.run(debug=True)

