# pip install SQLAlchemy mysql-connector-python pandas xlrd

import os
import csv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'mysql+mysqlconnector://root:root@localhost:3306/elector'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class MonthlyElectorate(Base):
    __tablename__ = 'MonthlyElectorate'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer)
    marital_status = Column(String(255))
    age_range = Column(String(255))
    gender = Column(String(255))
    education_level = Column(String(255))
    month = Column(Integer)
    city = Column(String(255))
    country = Column(String(255))
    region = Column(String(255))
    situation = Column(String(255))
    censo_uf = Column(String(255))
    zone = Column(Integer)
    elector_quantity = Column(Integer)
    load_date = Column(String(255))

def load_data_from_csv(filename):

    Base.metadata.create_all(engine)
    batch_size = 1000  # Tamanho do lote
    data_to_insert = []

    with open(filename, mode='r', encoding='latin-1') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            elector = MonthlyElectorate(
                year=int(row['Ano']),
                marital_status=row['Estado civil'],
                age_range=row['Faixa etária'],
                gender=row['Gênero'],
                education_level=row['Grau de instrução'],
                month=int(row['Mês']),
                city=row['Município'],
                country=row['País'],
                region=row['Região'],
                situation=row['Situação do eleitor'],
                censo_uf=row['UF'],
                zone=int(row['Zona']),
                elector_quantity=int(row['Quantidade de eleitor']),
                load_date=row['Data de carga']
            )
            data_to_insert.append(elector)

            if len(data_to_insert) >= batch_size:
                insert_batch(data_to_insert)
                data_to_insert = []

    if data_to_insert:
        insert_batch(data_to_insert)

def insert_batch(data):
    session = SessionLocal()
    try:
        session.bulk_save_objects(data)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Erro ao inserir lote: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    csv_filename = os.path.abspath('/Users/tony/Downloads/eleitorado_mensal.csv')

    # Carrega dados do arquivo CSV
    load_data_from_csv(csv_filename)
