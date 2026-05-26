from flask import Blueprint, render_template
from app.models.equipo import Equipo
from app.models.alerta import Alerta

dashboard_bp = Blueprint(
    'dashboard',
    __name__
)

@dashboard_bp.route('/')
def dashboard():

    equipos = Equipo.query.all()

    total_equipos = len(equipos)

    online = 0
    offline = 0

    total_cpu = 0
    equipos_cpu = 0

    for equipo in equipos:

        # ONLINE / OFFLINE
        if equipo.estado == 'Online':

            online += 1

        else:

            offline += 1

        # CPU PROMEDIO
        if equipo.cpu_actual is not None:

            total_cpu += equipo.cpu_actual
            equipos_cpu += 1

    # EVITAR DIVISIÓN ENTRE 0
    if equipos_cpu > 0:

        cpu_promedio = round(
            total_cpu / equipos_cpu,
            2
        )

    else:

        cpu_promedio = 0

    ultimas_alertas = Alerta.query.order_by(
    Alerta.fecha.desc()
    ).limit(5).all()
    
    return render_template(
        'dashboard/index.html',
    total_equipos=total_equipos,
    online=online,
    offline=offline,
    cpu_promedio=cpu_promedio,
    equipos=equipos,
    ultimas_alertas=ultimas_alertas
    )