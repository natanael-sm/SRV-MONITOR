from flask import Blueprint, render_template
from app.models.equipo import Equipo

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard():
    total_equipos = Equipo.query.count()
    equipos_online = Equipo.query.filter_by(estado='Online').count()
    equipos_offline = Equipo.query.filter_by(estado='Offline').count()

    return render_template(
        'dashboard/index.html',
        total_equipos=total_equipos,
        equipos_online=equipos_online,
        equipos_offline=equipos_offline
    )
