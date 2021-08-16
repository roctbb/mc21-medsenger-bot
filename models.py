from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_comment = db.Column(db.Text)
    address = db.Column(db.Text, nullable=True)
    card = db.Column(db.String(255), nullable=True)
    alerts = db.relationship('Alert', backref=backref('contract', uselist=False), lazy=True)


class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.id', ondelete="CASCADE"))
    age = db.Column(db.Integer)
    name = db.Column(db.String(255))
    birthday = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    scenario = db.Column(db.String(255))
    message = db.Column(db.Text)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    sent_on = db.Column(db.DateTime, nullable=True)
    done_on = db.Column(db.DateTime, nullable=True)
    closed_on = db.Column(db.DateTime, nullable=True)

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
            "sent_answer": self.result,
            "sent_comment": self.comment,
            "message": self.message,
            "comment": self.contract.doctor_comment,
            "address": self.contract.address,
            "card": self.contract.card,
            "scenario": self.scenario,
            "comment_options": [
                "Отправлена скорая помощь",
                "Нет возможности вызова СМП, предложен вызов 03",
                "Пациент отказался от вызова скорой помощи",
                "Пациент ввел ошибочные данные",
                "Не удалось дозвониться",
                "Другое",
            ]
        }


class Workstation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_key = db.Column(db.String(255))
    description = db.Column(db.String(255))
