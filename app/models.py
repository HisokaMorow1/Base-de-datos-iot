from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Table,
    Float,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# Tabla de asociación para la relación muchos-a-muchos entre Dispositivo y GrupoDispositivos
dispositivo_grupo = Table(
    "dispositivo_grupo",
    Base.metadata,
    Column("dispositivo_id", Integer, ForeignKey("dispositivo.id"), primary_key=True),
    Column("grupo_id", Integer, ForeignKey("grupo_dispositivos.id"), primary_key=True),
)

class TipoDispositivo(Base):
    __tablename__ = "tipo_dispositivo"

    id = Column(Integer, primary_key=True)
    fabricante = Column(String, nullable=False)
    modelo = Column(String, unique=True, nullable=False)
    descripcion = Column(Text)

    dispositivos = relationship("Dispositivo", back_populates="tipo_dispositivo")

class GrupoDispositivos(Base):
    __tablename__ = "grupo_dispositivos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(Text)

    dispositivos = relationship(
        "Dispositivo",
        secondary=dispositivo_grupo,
        back_populates="grupos"
    )

class Dispositivo(Base):
    __tablename__ = "dispositivo"

    id = Column(Integer, primary_key=True)
    numero_serie = Column(String, unique=True, nullable=False)
    mac_address = Column(String, unique=True)
    version_firmware = Column(String, nullable=False)
    descripcion_ubicacion = Column(String, nullable=False)
    coordenadas_gps = Column(String)  # formato "lat,lon"
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    tipo_dispositivo_id = Column(Integer, ForeignKey("tipo_dispositivo.id"), nullable=False)
    estado_actual = Column(String)  # agregado en modificación de esquema

    tipo_dispositivo = relationship("TipoDispositivo", back_populates="dispositivos")
    sensores = relationship("Sensor", back_populates="dispositivo")
    logs_estado = relationship("LogEstadoDispositivo", back_populates="dispositivo")
    grupos = relationship(
        "GrupoDispositivos",
        secondary=dispositivo_grupo,
        back_populates="dispositivos"
    )

class Sensor(Base):
    __tablename__ = "sensor"

    id = Column(Integer, primary_key=True)
    dispositivo_id = Column(Integer, ForeignKey("dispositivo.id"), nullable=False)
    tipo_sensor = Column(String, nullable=False)  # ej. 'temperatura', 'humedad'
    unidad_medida = Column(String, nullable=False)  # ej. '°C', '%'
    umbral_alerta = Column(Float)  # agregado en modificación de esquema

    dispositivo = relationship("Dispositivo", back_populates="sensores")
    lecturas = relationship("LecturaDato", back_populates="sensor")

class LecturaDato(Base):
    __tablename__ = "lectura_dato"

    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey("sensor.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    valor_leido = Column(String, nullable=False)  # usar String para flexibilidad

    sensor = relationship("Sensor", back_populates="lecturas")

class LogEstadoDispositivo(Base):
    __tablename__ = "log_estado_dispositivo"

    id = Column(Integer, primary_key=True)
    dispositivo_id = Column(Integer, ForeignKey("dispositivo.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    estado = Column(String, nullable=False)  # ej. 'online', 'offline', etc.
    mensaje_opcional = Column(Text)

    dispositivo = relationship("Dispositivo", back_populates="logs_estado")