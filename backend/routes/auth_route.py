from flask import Blueprint, request, jsonify, session
from ..models.family_model import Family
from ..models.member_model import Member
from ..extensions import db

bp = Blueprint("auths", __name__, url_prefix="/api/auth")

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    if Family.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 409
    
    try:
        family = Family(email=data["email"])
        family.set_password(data["password"])
        db.session.add(family)
        db.session.flush()
        db.session.commit()
        
        session["family_id"] = family.id
        session["logged_in"] = True
        
        return jsonify({"success": True,"family_id": family.id}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Registration failed"}), 500
    

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing email or password"}), 400
    
    family = Family.query.filter_by(email=data["email"]).first()
    
    if not family or not family.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401
    
    session["family_id"] = family.id
    session["logged_in"] = True
    
    return jsonify({
        "success": True,
        "family_id": family.id
    })

@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True})

@bp.route("/verify-member", methods=["POST"])
def verify_member():
    if "family_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    if "member_id" not in data:
        return jsonify({"error": "Missing member ID"}), 400
    
    member = Member.query.filter_by(
        id=data["member_id"],
        family_id=session["family_id"]).first()
    
    if not member:
        return jsonify({"error": "Member not found"}), 404
    
    if member.role == "parent" and member.has_password:
        if "password" not in data:
            return jsonify({"error": "Password required", "requires_password": True}), 401
        
        if not member.check_password(data["password"]):
            return jsonify({"error": "Invalid password"}), 401
    
    # Set member session
    session["member_id"] = member.id
    session["member_name"] = member.name
    session["member_role"] = member.role
    
    return jsonify({
        "success": True,
        "member": {
            "id": member.id,
            "name": member.name,
            "role": member.role
        }
    })

@bp.route("/set-password", methods=["POST"])
def set_password():
    if "member_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    if "password" not in data:
        return jsonify({"error": "Password required"}), 400
    
    member = Member.query.get(session["member_id"])
    if not member or member.family_id != session["family_id"]:
        return jsonify({"error": "Member not found"}), 404
    
    if member.role != "parent":
        return jsonify({"error": "Only parents can set passwords"}), 403
    
    member.set_password(data["password"])
    db.session.commit()
    return jsonify({"success": True})
