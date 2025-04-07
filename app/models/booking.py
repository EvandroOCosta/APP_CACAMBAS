# app/models/booking.py
from config.database import db

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dumpster_id = db.Column(db.Integer, db.ForeignKey('dumpsters.id'), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "dumpster_id": self.dumpster_id,
            "start_date": self.start_date,
            "end_date": self.end_date
        }
