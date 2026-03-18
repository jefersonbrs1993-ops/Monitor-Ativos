from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Configuração do Banco de Dados
DATABASE_URL = "sqlite:///./ativos.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Definição da Tabela (Como o baú será organizado)
class Ativo(Base):
    __tablename__= "ativos"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String)  # Ex: PETR4
    quantidade = Column(Integer)
    preco_medio = Column(Float)

# Criar a tabela de verdade dentro do arquivo ativos.db
Base.metadata.create_all(bind=engine)

# 3. Iniciar o FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"status": "Banco de Dados Conectado e Tabela Criada!"}
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Configuração do Banco de Dados
DATABASE_URL = "sqlite:///./ativos.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Definição da Tabela (Como o baú será organizado)
class Ativo(Base):
    _tablename_ = "ativos"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String)  # Ex: PETR4
    quantidade = Column(Integer)
    preco_medio = Column(Float)

# Criar a tabela de verdade dentro do arquivo ativos.db
Base.metadata.create_all(bind=engine)

# 3. Iniciar o FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"status": "Banco de Dados Conectado e Tabela Criada!"}
# Rota para buscar todos os ativos que estão salvos no banco
@app.get("/ativos")
def listar_ativos():
    db = SessionLocal()
    # Aqui o Python diz: "Busque todos os registros dentro da tabela Ativo"
    lista = db.query(Ativo).all()
    db.close()
    return lista