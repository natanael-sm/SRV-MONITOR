from app import db
from datetime import datetime

class Alerta(db.Model):
    __tablename__='alertas'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    equipo_id =db.Column(
        db.Integer,
        db.ForeignKey('equipos.id')
    )
    tipo = db.Column(
        db.String(100)
    )
    mensaje = db.Column(
        db.String(255)
    )

    severidad = db.Column(
        db.String(50)
    )

    fecha = db.Column(
        db.DateTime,
        default=datetime.now
    )