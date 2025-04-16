# models/review.py
from config.database import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Review(db.Model):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    comment = Column(String(255), nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    dumpster_id = Column(Integer, ForeignKey('dumpsters.id'), nullable=False)

    user = relationship('User', backref='reviews')
    dumpster = relationship('Dumpster', backref='reviews')
