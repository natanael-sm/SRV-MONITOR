from app import db
from datetime import datetime

class Metrica(db.Model):
    __tablename__ = 'metricas'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    equipo_id = db.Column(
        db.Integer,
        db.ForeignKey('equipos.id')
    )

    cpu =db.Column(
        db.Float
    )

    ram = db.Column(
        db.Float
    )

    disco = db.Column(
        db.Float
    )

    fecha = db.Column(
        db.DateTime,
        default=datetime.now
    )