from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    family_id = db.Column(db.Integer, db.ForeignKey("familys.id"), nullable=False)
    name = db.Column(db.Sring(80), nullable=False)
    role = db.Column(db.Sring(20), nullable=False) # "parent" or "child"
    password = db.Column(db.Sring(200))

    famiy = db.relationship("Family", back_populates="members")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    @property
    def has_password(self):
        return self.password_hash is not None