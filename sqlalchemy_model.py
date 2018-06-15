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
    evidences = relationship('Evidence', backref='project', lazy='dynamic')

    def __repr__(self):
        str_created_at = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return "<Project (id='%s', name='%s', created_at=%s)>" % (self.id, self.name, str_created_at)


class Evidence(Base):
    __tablename__ = 'evidence'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String(1000))
    description = Column(String(3000))
    order = Column(Integer)
    project_id = Column(Integer, ForeignKey('project.id'))

    def __repr__(self):
        return "<Evidence (name='%s')>" % (self.name)


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
    engine = create_engine('sqlite:///database/my_db.sqlite', echo=True)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_database()