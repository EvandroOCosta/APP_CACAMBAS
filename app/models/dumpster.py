from config.database import db

class Dumpster(db.Model):
    __tablename__ = "dumpsters"

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(255), nullable=False)
    size = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "location": self.location,
            "size": self.size
        }
