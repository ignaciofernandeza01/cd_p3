from flask import Blueprint, request, jsonify
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError  # <- SQLAlchemy, no psycopg2
from flask_jwt_extended import jwt_required
from db import get_db
from models import Game

bp_games = Blueprint("games", __name__, url_prefix="/games")

def to_dict(g: Game):
    return {
        "id": g.id,
        "nombre": g.nombre,
        "foto": g.foto,
        "link": g.link,
        "descripcion": g.descripcion,
        "popularidad": g.popularidad,
        "trailer": g.trailer,
        "categoria": g.categoria,
        "created_at": g.created_at.isoformat() if g.created_at else None,
        "updated_at": g.updated_at.isoformat() if g.updated_at else None,
    }

@bp_games.get("")  # o "/" si prefieres
def list_games():
    q = request.args.get("q")
    with next(get_db()) as db:
        stmt = select(Game)
        if q:
            like = f"%{q}%"
            stmt = stmt.where(Game.nombre.ilike(like))  # <- where, no filter sobre el select
        rows = db.execute(stmt.order_by(Game.id.desc())).scalars().all()
        return jsonify([to_dict(g) for g in rows])

@bp_games.get("/<int:game_id>")
def get_game(game_id: int):
    with next(get_db()) as db:
        g = db.get(Game, game_id)
        if not g:
            return jsonify({"msg": "no encontrado"}), 404
        return jsonify(to_dict(g))

@bp_games.post("")
@jwt_required()
def create_game():
    data = request.get_json() or {}
    if not data.get("nombre"):
        return jsonify({"msg": "nombre es obligatorio"}), 400

    with next(get_db()) as db:
        g = Game(
            nombre=data["nombre"],
            foto=data.get("foto"),
            link=data.get("link"),
            descripcion=data.get("descripcion"),
            popularidad=data.get("popularidad"),
            trailer=data.get("trailer"),
            categoria=data.get("categoria"),
        )
        try:
            db.add(g)
            db.commit()
            db.refresh(g)
            return jsonify(to_dict(g)), 201
        except IntegrityError:
            db.rollback()
            return jsonify({"error": "El juego ya existe (nombre único)."}), 409

@bp_games.put("/<int:game_id>")
@bp_games.patch("/<int:game_id>")
@jwt_required()
def update_game(game_id: int):
    data = request.get_json() or {}
    with next(get_db()) as db:
        g = db.get(Game, game_id)
        if not g:
            return jsonify({"msg": "no encontrado"}), 404
        for f in ("nombre", "foto", "link", "descripcion", "popularidad", "trailer", "categoria"):
            if f in data:
                setattr(g, f, data[f])
        db.commit()
        db.refresh(g)
        return jsonify(to_dict(g))

@bp_games.delete("/<int:game_id>")
@jwt_required()
def delete_game(game_id: int):
    with next(get_db()) as db:
        g = db.get(Game, game_id)
        if not g:
            return jsonify({"msg": "no encontrado"}), 404
        db.delete(g)
        db.commit()
        return "", 204
