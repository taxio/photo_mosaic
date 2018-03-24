from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, REAL
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class MaterialImage(Base):
    
    __tablename__ = 'materials'

    id_ = Column(Integer, primary_key=True)
    name = Column(String)
    R = Column(REAL)
    G = Column(REAL)
    B = Column(REAL)

    def __repr__(self):
        return '<Material(name=\'{}\', (R, G, B)=({}, {}, {}))>'.format(self.name, self.R, self.G, self.B)


class DBManager:

    def __init__(self, dbname: str, debug=False):
        self._engine = create_engine('sqlite:///'+dbname, echo=debug)
        Base.metadata.create_all(self._engine)
        Session = sessionmaker(bind=self._engine)
        self._session = Session()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_session()

    def close_session(self):
        self._session.close()

    def drop_table(self):
        Base.metadata.drop_all(self._engine)

    def insert_material(self, material):
        self._session.add(material)
        self._session.commit()

    def insert_all_material(self, materials):
        for mat in materials:
            self._session.add(mat)
        self._session.commit()
    
    def get_materials(self):
        return self._session.query(MaterialImage).all()

