from app import db
from datetime import datetime
datetime.now()

class Equipo(db.Model):

    __tablename__ = 'equipos'

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(100))
    ip = db.Column(db.String(50))
    sistema_operativo = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    
    ultimo_checkin = db.Column(db.DateTime, default=datetime.utcnow)
    cpu_actual = db.Column(db.Float, default=0)
    ram_actual = db.Column(db.Float, default=0)
    disco_actual = db.Column(db.Float, default=0)