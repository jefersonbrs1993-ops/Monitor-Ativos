from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Configuração do Banco de Dados (SQLite)
DATABASE_URL = "sqlite:///./ativos.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Definição da Tabela no Banco de Dados
class Ativo(Base):
    __tablename__ = "ativos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    tipo = Column(String)
    valor = Column(Float)

# Criar a tabela se ela não existir
Base.metadata.create_all(bind=engine)

# 3. Esquema de Validação (O que o usuário envia)
class AtivoCreate(BaseModel):
    nome: str
    tipo: str
    valor: float

# 4. Instância do FastAPI
app = FastAPI(title="Monitor de Ativos Industriais")

# 5. Rotas da API

@app.get("/")
def home():
    return {"status": "Servidor Rodando", "database": "Conectado"}

@app.post("/ativos")
def criar_ativo(ativo: AtivoCreate):
    db = SessionLocal()
    novo_ativo = Ativo(nome=ativo.nome, tipo=ativo.tipo, valor=ativo.valor)
    db.add(novo_ativo)
    db.commit()
    db.refresh(novo_ativo)
    db.close()
    return {"mensagem": "Ativo cadastrado com sucesso!", "dados": novo_ativo}

@app.get("/ativos")
def listar_ativos():
    db = SessionLocal()
    lista = db.query(Ativo).all()
    db.close()
    return lista
