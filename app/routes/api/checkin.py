from flask import Blueprint, request, jsonify
from app.models.equipo import Equipo
from app import db
from datetime import datetime
from app.models.metrica import Metrica
from app.models.alerta import Alerta

api_bp = Blueprint('api',__name__)

@api_bp.route('/api/equipos/checkin', methods=['POST'])
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

    # SI EL EQUIPO NO EXISTE
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

        # GENERAR ID SIN COMMIT
        db.session.flush()

    else:

        # ACTUALIZAR EQUIPO
        equipo.ip = ip
        equipo.sistema_operativo = sistema_operativo
        equipo.estado = estado

        equipo.cpu_actual = cpu_actual
        equipo.ram_actual = ram_actual
        equipo.disco_actual = disco_actual

        equipo.ultimo_checkin = datetime.now()

    # GUARDAR MÉTRICA
    nueva_metrica = Metrica(

        equipo_id=equipo.id,

        cpu=cpu_actual,
        ram=ram_actual,
        disco=disco_actual

    )

    db.session.add(nueva_metrica)

    # ALERTA CPU WARNING
    if cpu_actual >= 80:

        alerta_cpu = Alerta(

            equipo_id=equipo.id,

            tipo='CPU',

            mensaje=f'CPU Alta detectada: {cpu_actual}%',

            severidad='Warning'

        )

        db.session.add(alerta_cpu)

    # ALERTA CPU CRÍTICA
    if cpu_actual >= 95:

        alerta_cpu_critica = Alerta(

            equipo_id=equipo.id,

            tipo='CPU',

            mensaje=f'CPU crítica detectada: {cpu_actual}%',

            severidad='Critical'

        )

        db.session.add(alerta_cpu_critica)

    db.session.commit()

    return jsonify({
        'mensaje': 'Check-in recibido'
    })
