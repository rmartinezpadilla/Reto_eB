from config.bd import Base
from sqlalchemy import Column, String, DateTime

class Battle(Base): #modelo de asesor que representa la tabla en la base de datos
    #es necesaria para que la herramienta sqlalchemy pueda conocer las tablas
    __tablename__='battles'    
    uuid = Column(String(255), primary_key=True)    
    name_pokemon_a = Column(String(255),nullable=False, unique=True)
    name_pokemon_b = Column(String(255),nullable=False, unique=True)
    winner_name_pokemon = Column(String(255),nullable=False, unique=True)  
    created_at = Column(DateTime)    
    updated_at = Column(DateTime)