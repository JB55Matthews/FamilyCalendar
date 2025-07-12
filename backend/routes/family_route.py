from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from flask.views import MethodView
from models.family_model import Family
from extensions import db

bp = Blueprint("familys", __name__)

@bp.route("/familys", methods=["GET"])
@jwt_required
def get_familys():
    familys = Family.query.all()