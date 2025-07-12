from extensions import db

class Family(db.Model):
    __tablename__ = "familys"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200))