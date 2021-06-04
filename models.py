from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_comments = db.Column(db.Text)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer)
    age = db.Column(db.Integer)
    name = db.Column(db.String(255))
    birthday = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    scenario = db.Column(db.String(255))
    message = db.Column(db.Text)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    sent_on = db.Column(db.DateTime, nullable=True)
    done_on = db.Column(db.DateTime, nullable=True)

    result = db.Column(db.String(255))
    comment = db.Column(db.Text)

    workstation_id = db.Column(db.Integer, db.ForeignKey('workstation.id', ondelete="CASCADE"), nullable=True)

    def as_dict(self):
        return {
            "id": self.id,
            "contract_id": self.contract_id,
            "name": self.name,
            "age": self.age,
            "birthday": self.birthday,
            "phone": self.phone,
            "created_on": self.created_on.strftime("%Y-%m-%d %H:%M:%S"),
            "message": self.message
        }

class Workstation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_key = db.Column(db.String(255))
    description = db.Column(db.String(255))