from sqlalchemy import create_engine, String, Text, Integer, Float, ForeignKey, delete, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship, sessionmaker
from typing import List, Optional
import os 
from dotenv import load_dotenv 

class Base(DeclarativeBase):
    pass

class Aviao(Base):
    __tablename__ = "aviao"
    id_aviao: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    modelo_aviao: Mapped[str] = mapped_column(String(250), nullable=False)
    compainha_aviao: Mapped[str] = mapped_column(String(250), nullable=False)
    capacidade_aviao: Mapped[str] = mapped_column(String(250), nullable=False)
    
    trajetos: Mapped[list["Trajeto"]] = relationship(
        back_populates="aviao", 
        cascade="all, delete-orphan" 
    )
   
class Trajeto(Base):
    __tablename__ = "trajeto"
    id_trajeto: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome_trajeto: Mapped[str] = mapped_column(String(250), nullable=False)
    tempo_trajeto: Mapped[str] = mapped_column(String(250), nullable=False)
    id_aviao: Mapped[int] = mapped_column(
            ForeignKey("aviao.id_aviao", ondelete='CASCADE'), nullable=False)
    
    aviao: Mapped["Aviao"] = relationship(back_populates="trajetos")
    
load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

engine_mysql = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}")
engine_sqllite = create_engine("sqlite:///avioes.db")

@event.listens_for(engine_sqllite, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

engine = None
r = True
while r == True:
    print("Bem-vindo(a)!")
    print("Qual banco de dados você quer usar?\n1- MySQL\n2- SQLlite")
    resposta=int(input())
    if resposta == 1:
        engine=engine_mysql 
    if resposta == 2:
            engine=engine_sqllite
    
    Base.metadata.create_all(engine)
    print("O que você gostaria de fazer?\n1- Inserir\n2- Listar\n3- Excluir")
    resposta=int(input())
    Session = sessionmaker(bind=engine)
    session = Session()
    if resposta == 1:
        print("Em qual tabela você quer inserir?\n1- Avião\n2-Trajeto")
        resposta=int(input())
        if resposta == 1: 
            print("Informe: modelo, compainha e capacidade")
            modelo= str(input())
            compainha= str(input())
            capacidade= str(input())
            novo_aviao= Aviao(modelo_aviao= modelo, compainha_aviao= compainha, capacidade_aviao= capacidade)
            session.add(novo_aviao)
            session.commit()
        if resposta == 2: 
            print("Informe: nome, tempo e id do aviao")
            nome= str(input())
            tempo= str(input())
            id_aviao= int(input())
            novo_trajeto= Trajeto(nome_trajeto= nome, tempo_trajeto= tempo, id_aviao= id_aviao)
            session.add(novo_trajeto)
            session.commit()
    if resposta == 2:
        avioes = session.query(Aviao).all()
        trajetos = session.query(Trajeto).all()
        print("Aviões:")
        for a in avioes:
            print(f"ID: {a.id_aviao} | Modelo: {a.modelo_aviao} | Compainha: {a.compainha_aviao} | Capacidade: {a.capacidade_aviao}") 
        print("Trajetos:")
        for a in trajetos:
                    print(f"ID Trajeto: {a.id_trajeto} | ID Aviao: {a.id_aviao} | Nome: {a.nome_trajeto} | Tempo: {a.tempo_trajeto}")
    if resposta == 3:
        print("De qual tabela você quer deletar?\n1- Aviao\n2- Trajeto")
        resposta= int(input())
        if resposta == 1:
            print("Informe o id do avião que quer deletar:")
            id_aviao= int(input())
            stmt= delete(Aviao).where(Aviao.id_aviao == id_aviao)
            session.execute(stmt)
            session.commit()
            print("Avião foi deletado!")
    print("Gostaria de continuar?\n1- Sim\n2- Não")
    resposta=int(input())
    if resposta == 2: 
        r = False
    