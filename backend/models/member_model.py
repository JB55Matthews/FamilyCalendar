from extensions import db

class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    family_id = db.Column(db.Integer, db.ForeignKey("familys.id"), nullable=False)
    name = db.Column(db.Sring(80), nullable=False)
    role = db.Column(db.Sring(20), nullable=False) # "parent" or "child"
    password = db.Column(db.Sring(200))

    famiy = db.relationship("Family", back_populates="members")