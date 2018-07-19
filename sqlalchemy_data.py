# ----------------------------
# Turn Foreign Key Constraints ON for
# each connection.
# ----------------------------
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_model import Proof, ProofType, Finding, Project
from datetime import datetime
import os

session = None


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create(element):
    session.add(element)
    session.commit()
    return element


def delete(element):
    session.delete(element)
    session.commit()


def commit_changes():
    session.commit()


def get_proof_types():
    return session.query(ProofType).all()


def get_proof_type_by_name(name):
    return session.query(ProofType).filter(ProofType.name == name).one_or_none()


def get_all_proofs():
    return session.query(Proof).all()


def get_finding_by_id(finding_id):
    return session.query(Finding).filter(Finding.id == finding_id)


def get_findings_by_project_name(project_id):
    return session.query(Finding).filter(Finding.project_id == project_id).all()


def get_project_by_name(project_name):
    return session.query(Project).filter(Project.name == project_name).one_or_none()


def get_all_projects():
    return session.query(Project).all()


def populate_database(database='db'):
    global session
    engine = create_engine('sqlite:///database/{}.sqlite'.format(database), echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()


    if not os.path.exists('database/{}.sqlite'.format(database)):
        print('Database selected does not exist. Create it first')
        return
    else:
        proof_types = ['text', 'image', 'other']
        for proof_type in proof_types:
            if not get_proof_type_by_name(proof_type):
                create(ProofType(name=proof_type))
        commit_changes()
        print('Database successfully populated')


# proof1 = Proof(type=get_proof_type_by_name('text'),
#                path='/root/Desktop/test.txt')
# proof2 = Proof(type=get_proof_type_by_name('text'),
#                path='/root/Desktop/test222222.txt')
#
# finding_1 = Finding(name='new_finding',
#                     file_path='asdf',
#                     description='lasdkfasd alkdf asdf adf ajdsf kasdf asdf ladksf lakjsdf lkajsdf',
#                     proofs=[proof1, proof2])
#
# project_66 = Project(name='jejejej',
#                      description="my general description",
#                      findings=[finding_1])
#
# create(project_66)
# print(get_all_proofs())
