# ----------------------------
# Turn Foreign Key Constraints ON for
# each connection.
# ----------------------------
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_model import Evidence, Project
from datetime import datetime


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


engine = create_engine('sqlite:///database/my_db.sqlite', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def create(element):
    session.add(element)
    session.commit()
    return element


def delete(element):
    session.delete(element)
    session.commit()


def commit_changes():
    session.commit()


def get_evidence_by_id(evidence_id):
    return session.query(Evidence).filter(Evidence.id == evidence_id)


def get_evidences_by_project_name(project_id):
    return session.query(Evidence).filter(Evidence.project_id == project_id).all()


def get_project_by_name(project_name):
    return session.query(Project).filter(Project.name == project_name).one_or_none()


def get_all_projects():
    return session.query(Project).all()

# ----------------------------
# Populate the database
# ----------------------------
# evidence_1 = Evidence(name='ualalala')
# evidence_2 = Evidence(name='ssssssss')
#
# project_66 = Project(name='myprojectGOOOOD',
#                      description="my general description",
#                      evidences=[evidence_1, evidence_2])
