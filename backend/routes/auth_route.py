from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from ..models.family_model import Family
from ..models.member_model import Member
from ..extensions import db

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.json()
        required = ["email", "password"]

        if not all(key in data for key in required):
            abort(400, message="Missing fields")

        if Family.query.filter_by(email=data["email"]).first():
            abort(409, message="Email already registered")
        
        family = Family(email=data["email"])
        family.set_password(data["password"])

        db.session.add(family)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        abort(500, message="Internal error while creating family")
    
    access_token = create_access_token(identity={
        "family_id": family.id
    })

    return jsonify({
        "access_token": access_token,
        "family_id": family.id
    })

@bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.json()
        family = Family.query.filter_by(email=data["email"]).first()
        if (family is None) or (not family.check_password(data["password"])):
            abort(401, message="Invalid credentials")
    except SQLAlchemyError:
        abort(500, "Internal server error")
    
    access_token = create_access_token(identity={
        "family_id": family.id
    })

    return jsonify({
        "access_token": access_token,
        "family_id": family.id
    })