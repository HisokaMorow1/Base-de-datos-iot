from sqlalchemy.orm import Session
from app import models
from sqlalchemy import select

# --- TipoDispositivo ---
def crear_tipo_dispositivo(db: Session, fabricante: str, modelo: str, descripcion: str = None):
    tipo = models.TipoDispositivo(fabricante=fabricante, modelo=modelo, descripcion=descripcion)
    db.add(tipo)
    db.commit()
    db.refresh(tipo)
    return tipo

def obtener_tipos_dispositivo(db: Session):
    return db.query(models.TipoDispositivo).all()

# --- GrupoDispositivos ---
def crear_grupo_dispositivos(db: Session, nombre: str, descripcion: str = None):
    grupo = models.GrupoDispositivos(nombre=nombre, descripcion=descripcion)
    db.add(grupo)
    db.commit()
    db.refresh(grupo)
    return grupo

def obtener_grupos_dispositivos(db: Session):
    return db.query(models.GrupoDispositivos).all()

# --- Dispositivo ---
def crear_dispositivo(db: Session, numero_serie: str, version_firmware: str, descripcion_ubicacion: str,
                     tipo_dispositivo_id: int, mac_address: str = None, coordenadas_gps: str = None):
    dispositivo = models.Dispositivo(
        numero_serie=numero_serie,
        version_firmware=version_firmware,
        descripcion_ubicacion=descripcion_ubicacion,
        tipo_dispositivo_id=tipo_dispositivo_id,
        mac_address=mac_address,
        coordenadas_gps=coordenadas_gps
    )
    db.add(dispositivo)
    db.commit()
    db.refresh(dispositivo)
    return dispositivo

def obtener_dispositivos(db: Session):
    return db.query(models.Dispositivo).all()

def obtener_dispositivos_por_tipo(db: Session, tipo_dispositivo_id: int):
    return db.query(models.Dispositivo).filter_by(tipo_dispositivo_id=tipo_dispositivo_id).all()

def obtener_dispositivos_por_grupo(db: Session, grupo_id: int):
    grupo = db.query(models.GrupoDispositivos).filter_by(id=grupo_id).first()
    return grupo.dispositivos if grupo else []

def asociar_dispositivo_a_grupo(db: Session, dispositivo_id: int, grupo_id: int):
    dispositivo = db.query(models.Dispositivo).filter_by(id=dispositivo_id).first()
    grupo = db.query(models.GrupoDispositivos).filter_by(id=grupo_id).first()
    if dispositivo and grupo and grupo not in dispositivo.grupos:
        dispositivo.grupos.append(grupo)
        db.commit()
    return dispositivo

def desasociar_dispositivo_de_grupo(db: Session, dispositivo_id: int, grupo_id: int):
    dispositivo = db.query(models.Dispositivo).filter_by(id=dispositivo_id).first()
    grupo = db.query(models.GrupoDispositivos).filter_by(id=grupo_id).first()
    if dispositivo and grupo and grupo in dispositivo.grupos:
        dispositivo.grupos.remove(grupo)
        db.commit()
    return dispositivo

def obtener_grupos_de_dispositivo(db: Session, dispositivo_id: int):
    dispositivo = db.query(models.Dispositivo).filter_by(id=dispositivo_id).first()
    return dispositivo.grupos if dispositivo else []

# --- Sensor ---
def crear_sensor(db: Session, dispositivo_id: int, tipo_sensor: str, unidad_medida: str, umbral_alerta: float = None):
    sensor = models.Sensor(
        dispositivo_id=dispositivo_id,
        tipo_sensor=tipo_sensor,
        unidad_medida=unidad_medida,
        umbral_alerta=umbral_alerta
    )
    db.add(sensor)
    db.commit()
    db.refresh(sensor)
    return sensor

def obtener_sensores_de_dispositivo(db: Session, dispositivo_id: int):
    return db.query(models.Sensor).filter_by(dispositivo_id=dispositivo_id).all()

# --- LecturaDato ---
def crear_lectura_dato(db: Session, sensor_id: int, valor_leido: str):
    lectura = models.LecturaDato(sensor_id=sensor_id, valor_leido=valor_leido)
    db.add(lectura)
    db.commit()
    db.refresh(lectura)
    return lectura

def obtener_ultimas_lecturas(db: Session, sensor_id: int, n: int = 10):
    return (
        db.query(models.LecturaDato)
        .filter_by(sensor_id=sensor_id)
        .order_by(models.LecturaDato.timestamp.desc())
        .limit(n)
        .all()
    )

# --- LogEstadoDispositivo ---
def crear_log_estado(db: Session, dispositivo_id: int, estado: str, mensaje_opcional: str = None):
    log = models.LogEstadoDispositivo(
        dispositivo_id=dispositivo_id,
        estado=estado,
        mensaje_opcional=mensaje_opcional
    )
    db.add(log)
    # Actualiza el estado_actual del dispositivo
    dispositivo = db.query(models.Dispositivo).filter_by(id=dispositivo_id).first()
    if dispositivo:
        dispositivo.estado_actual = estado
    db.commit()
    db.refresh(log)
    return log

def obtener_logs_de_dispositivo(db: Session, dispositivo_id: int):
    return (
        db.query(models.LogEstadoDispositivo)
        .filter_by(dispositivo_id=dispositivo_id)
        .order_by(models.LogEstadoDispositivo.timestamp.desc())
        .all()
    )