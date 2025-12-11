from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from db import get_db
from models import User

bp_auth = Blueprint("auth", __name__, url_prefix="/auth")

@bp_auth.post("/register")
def register():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password")
    if not email or not password:
        return jsonify({"msg": "email y password son obligatorios"}), 400
    with next(get_db()) as db:
        u = User(email=email)
        u.set_password(password)
        db.add(u)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            return jsonify({"msg": "email ya registrado"}), 409
    return jsonify({"msg": "usuario creado"}), 201

@bp_auth.post("/login")
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password")
    if not email or not password:
        return jsonify({"msg": "email y password son obligatorios"}), 400
    with next(get_db()) as db:
        u = db.query(User).filter_by(email=email).first()
        if not u or not u.check_password(password):
            return jsonify({"msg": "credenciales inválidas"}), 401
    token = create_access_token(identity=email)  # el 'sub' del token será el email
    return jsonify({"access_token": token})

@bp_auth.get("/me")
@jwt_required()
def me():
    # ejemplo de ruta protegida
    return jsonify({"email": get_jwt_identity()})

