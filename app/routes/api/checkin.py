from flask import Blueprint, request, jsonify
from app.models.equipo import Equipo
from app import db
from datetime import datetime

api_bp = Blueprint('api',__name__)

@api_bp.route('/api/equipos/checkin', methods=['POST'])
def checkin():

    data = request.get_json()

    hostname = data.get('hostname')
    ip = data.get('ip')
    sistema_operativo = data.get('sistema_operativo')
    estado = data.get('estado')

    cpu_actual = data.get('cpu_actual', 0)
    ram_actual = data.get('ram_actual', 0)
    disco_actual = data.get('disco_actual', 0)

    equipo = Equipo.query.filter_by(
        hostname=hostname
    ).first()

    if not equipo:

        equipo = Equipo(
            hostname=hostname,
            ip=ip,
            sistema_operativo=sistema_operativo,
            estado=estado,
            cpu_actual=cpu_actual,
            ram_actual=ram_actual,
            disco_actual=disco_actual,
            ultimo_checkin=datetime.now()
        )

        db.session.add(equipo)

    else:

        equipo.ip = ip
        equipo.sistema_operativo = sistema_operativo
        equipo.estado = estado

        equipo.cpu_actual = cpu_actual
        equipo.ram_actual = ram_actual
        equipo.disco_actual = disco_actual

        equipo.ultimo_checkin = datetime.now()

    db.session.commit()

    return jsonify({
        'mensaje': 'Check-in recibido'
    })
