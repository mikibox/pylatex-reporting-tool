#----------------------------
# Turn Foreign Key Constraints ON for
# each connection.
#----------------------------
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

#----------------------------
# Populate the database
#----------------------------

evidence_1 = Evidence(name='jejsssse')
evidence_2 = Evidence(name='ahhaaaah')

project_66 = Project(name='myprojectGOOOOD',
                     description="my general description",
                     evidences=[evidence_1, evidence_2])


# Create a new Session and add the images:
session = Session()

session.add(evidence_1)
session.add(evidence_2)
session.add(project_66)

# Commit the changes:
session.commit()
print("COMMIT OF THE CHANGES")
print(session.query(Project).all())
quit()

