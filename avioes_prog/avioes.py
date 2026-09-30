from sqlalchemy import create_engine, String, Text, Integer, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from typing import List, Optional
import os 
from dotenv import load_dotenv 

class Base(DeclarativeBase):
    pass

class Aviao(Base):
    __tablename__ = "aviao"
    id_aviao: Mapped[int] = mapped_column(primary_key=True)
    modelo_aviao: Mapped[str] = mapped_column(String(250))
    compainha_aviao: Mapped[int] = mapped_column(Integer)
    capacidade_aviao: Mapped[str] = mapped_column(String(120))
   

class Trajeto(Base):
    __tablename__ = "trajeto"
    id_trajeto: Mapped[int] = mapped_column(primary_key=True)
    nome_trajeto: Mapped[str] = mapped_column(String(250))
    tempo_trajeto: Mapped[str] = mapped_column(String(250))
    id_aviao: Mapped[int] = mapped_column(
            ForeignKey("aviao.id_aviao"), 
            primary_key=True)
    
load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

engine_mysql = create_engine("mysql+pymysql://root:@localhost:3306/aviao")
engine_sqllite = create_engine("sqlite:///pessoas.db")

engine = None

print("Bem-vindo(a)!")
print("Qual bando de dados você quer usar?"
      "1- MySQL"
      "2- SQLlite")
resposta=int(input())
if resposta == 1:
     engine=engine_mysql 
     Base.metadata.create_all(engine)
if resposta == 2:
    engine=engine_sqllite
    Base.metadata.create_all(engine)

