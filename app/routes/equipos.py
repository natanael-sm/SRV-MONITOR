from flask import Blueprint, render_template, request, redirect
from app.models.equipo import Equipo
from app import db
from datetime import datetime, timedelta

equipos_bp = Blueprint(
    'equipos',
    __name__
)

# LISTAR EQUIPOS
@equipos_bp.route('/equipos')
def listar_equipos():

    equipos = Equipo.query.all()

    ahora = datetime.now()

    for equipo in equipos:

        # SI NO TIENE CHECK-IN
        if equipo.ultimo_checkin is None:

            equipo.estado = 'Offline'
            continue

        diferencia = ahora - equipo.ultimo_checkin

        # SI EL CHECK-IN FUE HACE MÁS DE 24 HORAS
        if diferencia > timedelta(minutes=1440):

            equipo.estado = 'Offline'

        else:

            equipo.estado = 'Online'

    db.session.commit()

    return render_template(
        'equipos/index.html',
        equipos=equipos
    )


# FORMULARIO NUEVO EQUIPO
@equipos_bp.route('/equipos/nuevo')
def nuevo_equipo():

    return render_template(
        'equipos/nuevo.html'
    )


# GUARDAR EQUIPO
@equipos_bp.route('/equipos/guardar', methods=['POST'])
def guardar_equipo():

    hostname = request.form['hostname']
    ip = request.form['ip']
    sistema_operativo = request.form['sistema_operativo']
    estado = request.form['estado']

    nuevo_equipo = Equipo(
        hostname=hostname,
        ip=ip,
        sistema_operativo=sistema_operativo,
        estado=estado
    )

    db.session.add(nuevo_equipo)
    db.session.commit()

    return redirect('/equipos')

# EDITAR EQUIPO
@equipos_bp.route('/equipos/editar/<int:id>')
def editar_equipo(id):

    equipo = Equipo.query.get_or_404(id)

    return render_template(
        'equipos/editar.html',
        equipo=equipo
    )


# ACTUALIZAR EQUIPO
@equipos_bp.route('/equipos/actualizar/<int:id>', methods=['POST'])
def actualizar_equipo(id):

    equipo = Equipo.query.get_or_404(id)

    equipo.hostname = request.form['hostname']
    equipo.ip = request.form['ip']
    equipo.sistema_operativo = request.form['sistema_operativo']
    equipo.estado = request.form['estado']

    db.session.commit()

    return redirect('/equipos')


# ELIMINAR EQUIPO
@equipos_bp.route('/equipos/eliminar/<int:id>')
def eliminar_equipo(id):

    equipo = Equipo.query.get_or_404(id)

    db.session.delete(equipo)
    db.session.commit()

    return redirect('/equipos')