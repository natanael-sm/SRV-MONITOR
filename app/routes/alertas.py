from flask import Blueprint, render_template
from app.models.alerta import Alerta

alertas_bp = Blueprint(
    'alertas',
    __name__
)

@alertas_bp.route('/alertas')
def listar_alertas():

    alertas = Alerta.query.order_by(
        Alerta.fecha.desc()
    ).all()

    return render_template(
        'alertas/index.html',
        alertas=alertas
    )