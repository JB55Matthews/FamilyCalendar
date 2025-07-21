from flask import request, jsonify, session
from flask_smorest import Blueprint
from ..models.family_model import Family
from ..models.member_model import Member
from ..extensions import db

bp = Blueprint("familys", __name__, url_prefix="/api/family")

@bp.route("/members", methods=["GET"])
def get_family_members():
    if "family_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    members = Member.query.filter_by(family_id=db.session["family_id"]).all()
    members_data = []
    for member in members:
        # new_member = {
        #     "id": member.id,
        #     "display_name": member.name,
        #     "role": member.role,
        #     "has_password": member.has_password
        # }
        # members_data.append(new_member)
        members_data.append({
            "id": member.id,
            "display_name": member.name,
            "role": member.role,
            "has_password": member.has_password
        })
    return jsonify(members_data)

@bp.route("/add-member", methods=["POST"])
def add_family_member():
    if 'family_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    if not data or 'name' not in data or 'role' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    if data['role'] not in ['parent', 'child']:
        return jsonify({"error": "Invalid role"}), 400
    
    new_member = Member(
        family_id=session['family_id'],
        name=data['name'],
        role=data['role']
    )
    
    db.session.add(new_member)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "member_id": new_member.id
    })



    