from app.database import SessionLocal
import app.crud as crud

def main():
    db = SessionLocal()

    # Crear un tipo de dispositivo
    tipo = crud.crear_tipo_dispositivo(db, "Raspberry Pi", "RPi 4", "Mini PC para IoT")
    print("TipoDispositivo creado:", tipo.modelo)

    # Crear un grupo de dispositivos
    grupo = crud.crear_grupo_dispositivos(db, "Sensores Edificio A", "Sensores del edificio principal")
    print("GrupoDispositivos creado:", grupo.nombre)

    # Crear un dispositivo
    dispositivo = crud.crear_dispositivo(
        db,
        numero_serie="SN123456",
        version_firmware="1.0.0",
        descripcion_ubicacion="Oficina 101",
        tipo_dispositivo_id=tipo.id,
        mac_address="AA:BB:CC:DD:EE:FF",
        coordenadas_gps="-34.6037,-58.3816"
    )
    print("Dispositivo creado:", dispositivo.numero_serie)

    # Asociar el dispositivo al grupo
    crud.asociar_dispositivo_a_grupo(db, dispositivo.id, grupo.id)
    print("Dispositivo asociado al grupo.")

    # Crear un sensor
    sensor = crud.crear_sensor(db, dispositivo.id, "temperatura", "°C", umbral_alerta=30.0)
    print("Sensor creado:", sensor.tipo_sensor)

    # Crear una lectura de dato
    lectura = crud.crear_lectura_dato(db, sensor.id, "25.5")
    print("LecturaDato creada:", lectura.valor_leido)

    # Crear un log de estado
    log = crud.crear_log_estado(db, dispositivo.id, "online", "Dispositivo encendido correctamente")
    print("LogEstadoDispositivo creado:", log.estado)

    db.close()

if __name__ == "__main__":
    main()

    