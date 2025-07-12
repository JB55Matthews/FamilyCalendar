from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint
from models.family_model import Family
from models.member_model import Member
from extensions import db

bp = Blueprint("familys", __name__)

@bp.route("/familys", methods=["GET"])
@jwt_required
def get_family_members():
    identity = get_jwt_identity()
    family_id = identity["family_id"]
    members = Member.query.filter_by(family_id=family_id).all()
    members_data = []
    for member in members:
        members_data.append({
            "id": member.id,
            "display_name": member.name,
            "role": member.role,
            "has_password": member.has_password
        })
    
    return jsonify(members_data)