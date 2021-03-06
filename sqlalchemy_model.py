from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    findings = relationship('Finding', backref='project', lazy='dynamic')

    def __repr__(self):
        str_created_at = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return "<Project (id='%s', name='%s', created_at=%s)>" % (self.id, self.name, str_created_at)


class Finding(Base):
    __tablename__ = 'finding'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String(1000))
    description = Column(String(3000))
    order = Column(Integer)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    proofs = relationship('Proof')

    def __repr__(self):
        return "<Finding (name='%s')>" % (self.name)


class Proof(Base):
    __tablename__ = 'proof'
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('proof_type.id'))
    type = relationship('ProofType')
    path = Column(String(3000))
    finding_id = Column(Integer, ForeignKey('finding.id'), nullable=False)

    def __repr__(self):
        return "<Proof (type='{}', path '{}')>".format(self.type_id, self.path)


class ProofType(Base):
    __tablename__ = 'proof_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

    def __repr__(self):
        return self.name



# ----------------------------
# Turn Foreign Key Constraints ON for
# each connection.
# ----------------------------

from sqlalchemy.engine import Engine
from sqlalchemy import event


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_database():
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///database/my_db_tests.sqlite', echo=False)
    Base.metadata.create_all(engine)



if __name__ == '__main__':
    pass
