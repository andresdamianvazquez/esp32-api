from flask import Blueprint, render_template, redirect, url_for, flash, request, abort,jsonify
from flask_login import login_required, current_user
from app.models import Device, User, db, Device, Data
from datetime import datetime


main_bp = Blueprint('main', __name__)




@main_bp.route('/api/data/<int:device_id>', methods=['GET'])
def obtener_datos(device_id):
    # Parámetros opcionales para rango de fechas
    desde = request.args.get('desde')  # ejemplo: "2025-06-01T00:00:00"
    hasta = request.args.get('hasta')  # ejemplo: "2025-06-15T23:59:59"

    query = Data.query.filter_by(device_id=device_id)

    if desde:
        try:
            desde_dt = datetime.fromisoformat(desde)
            query = query.filter(Data.timestamp >= desde_dt)
        except ValueError:
            return jsonify({"error": "Formato inválido para 'desde'"}), 400

    if hasta:
        try:
            hasta_dt = datetime.fromisoformat(hasta)
            query = query.filter(Data.timestamp <= hasta_dt)
        except ValueError:
            return jsonify({"error": "Formato inválido para 'hasta'"}), 400

    resultados = query.order_by(Data.timestamp.desc()).all()

    datos_list = [{
        "timestamp": d.timestamp.isoformat(),
        "latitude": d.latitude,
        "longitude": d.longitude,
        "temperature": d.temperature,
        "humidity": d.humidity,
        "extra1": d.extra1,
        "extra2": d.extra2,
        "extra3": d.extra3,
        "extra4": d.extra4,
        "extra5": d.extra5,
        "extra6": d.extra6,
        "extra7": d.extra7,
        "extra8": d.extra8,
        "extra9": d.extra9,
        "extra10": d.extra10,
        "extra11": d.extra11,
        "extra12": d.extra12,
        "extra13": d.extra13,
        "extra14": d.extra14,
        "extra15": d.extra15,
        # Agregá extras si querés
    } for d in resultados]

    return jsonify(datos_list), 200



@main_bp.route('/api/data', methods=['POST'])
def recibir_datos():
    data = request.get_json()

    api_key = data.get("api_key")
    if not api_key:
        return jsonify({"error": "API key faltante"}), 400

    device = Device.query.filter_by(api_key=api_key).first()
    if not device:
        return jsonify({"error": "API key inválida"}), 401

    # Si llegamos acá, el dispositivo es válido
    # Podés ahora procesar los datos como quieras
    # Por ejemplo:
    timestamp_str = data.get("timestamp")
    try:
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else datetime.utcnow()
    except ValueError:
        return jsonify({"error": "Formato de timestamp inválido"}), 400

    # Creamos nuevo registro Data
    nuevo_dato = Data(
        device_id=device.id,
        timestamp=timestamp,
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        temperature=data.get("temperature"),
        humidity=data.get("humidity"),
        extra1=data.get("extra1"),
        extra2=data.get("extra2"),
        extra3=data.get("extra3"),
        extra4=data.get("extra4"),
        extra5=data.get("extra5"),
        extra6=data.get("extra6"),
        extra7=data.get("extra7"),
        extra8=data.get("extra8"),
        extra9=data.get("extra9"),
        extra10=data.get("extra10"),
        extra11=data.get("extra11"),
        extra12=data.get("extra12"),
        extra13=data.get("extra13"),
        extra14=data.get("extra14"),
        extra15=data.get("extra15"),
        # ... agregá los extras que quieras
    )

    db.session.add(nuevo_dato)
    db.session.commit()

    return jsonify({"mensaje": "Datos guardados correctamente"}), 201

@main_bp.route('/device/<int:device_id>/assign', methods=['GET', 'POST'])
@login_required
def assign_device(device_id):
    if not current_user.is_admin:
        abort(403)

    device    = Device.query.get_or_404(device_id)
    all_users = User.query.all()

    if request.method == 'POST':
        # user IDs seleccionados
        ids = request.form.getlist('users')
        device.users = User.query.filter(User.id.in_(ids)).all()
        db.session.commit()
        flash('Usuarios asignados correctamente', 'success')
        return redirect(url_for('main.device_detail', device_id=device_id))

    return render_template('assign_device.html',
                           device=device,
                           all_users=all_users)

@main_bp.route('/')
@login_required
def dashboard():
    if current_user.is_admin:
        dispositivos = Device.query.all()
    else:
        dispositivos = current_user.devices
    return render_template('dashboard.html', dispositivos=dispositivos)

@main_bp.route('/device/<int:device_id>')
@login_required
def device_detail(device_id):
    # Obtener el dispositivo o 404
    device = Device.query.get_or_404(device_id)
    # Verificar que el usuario sea admin o dueño del dispositivo
    if not (current_user.is_admin or device.owner_id == current_user.id):
        abort(403)

    # Traer los datos asociados, ordenados cronológicamente
    datos = Data.query.filter_by(device_id=device_id).order_by(Data.timestamp.desc()).limit(50).all()

    return render_template('device_detail.html',
                           device=device,
                           datos=datos)

@main_bp.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        new_username = request.form.get('username')
        is_admin = bool(request.form.get('is_admin'))
        if new_username:
            user.username = new_username
            user.is_admin = is_admin
            db.session.commit()
            flash('Usuario actualizado', 'success')
            return redirect(url_for('main.list_users'))
        flash('El nombre de usuario no puede estar vacío', 'danger')
    return render_template('edit_user.html', user=user)

@main_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('No podés borrarte a vos mismo', 'warning')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('Usuario borrado', 'success')
    return redirect(url_for('main.list_users'))






@main_bp.route('/users')
@login_required
def list_users():
    # Solo admins
    if not current_user.is_admin:
        abort(403)
    usuarios = User.query.all()
    return render_template('list_users.html', usuarios=usuarios)

@main_bp.route('/device/create', methods=['GET', 'POST'])
@login_required
def create_device():
    if not current_user.is_admin:
        abort(403)
    if request.method == 'POST':
        nombre = request.form.get('name')
        if not nombre:
            flash('El nombre del dispositivo es obligatorio', 'danger')
        else:
            nuevo = Device(name=nombre)
            # por defecto el admin creador se asigna
            nuevo.users.append(current_user)
            db.session.add(nuevo)
            db.session.commit()
            flash(f'Dispositivo "{nombre}" creado', 'success')
            return redirect(url_for('main.dashboard'))
    return render_template('create_device.html')

@main_bp.route('/user/create', methods=['GET', 'POST'])
@login_required
def create_user():
    if not current_user.is_admin:
        flash('Acceso denegado', 'warning')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Usuario y contraseña son obligatorios', 'danger')
        elif User.query.filter_by(username=username).first():
            flash('El usuario ya existe', 'warning')
        else:
            nuevo_usuario = User(username=username)
            nuevo_usuario.set_password(password)
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash(f'Usuario "{username}" creado con éxito', 'success')
            return redirect(url_for('main.dashboard'))
    return render_template('create_user.html')