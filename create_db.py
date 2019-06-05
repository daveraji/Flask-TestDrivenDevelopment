from app import db
from models import Flaskr

#creates database and db table
db.create_all()

#commites changes
db.session.commit()
