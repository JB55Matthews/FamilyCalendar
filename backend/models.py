from .extensions import Base
from sqlalchemy import *
from sqlalchemy.orm import (relationship)
from werkzeug.security import generate_password_hash, check_password_hash

class FamilyModel(Base):
    __tablename__ = "familys"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(200))

    members = relationship("MemberModel", back_populates="family")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class MemberModel(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    family_id = Column(Integer, ForeignKey("familys.id"), nullable=False)
    name = Column(String(80), nullable=False)
    role = Column(String(20), nullable=False) # "parent" or "child"
    password = Column(String(200))

    family = relationship("FamilyModel", back_populates="members")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    @property
    def has_password(self):
        return self.password_hash is not None