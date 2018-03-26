from flask_sqlalchemy import SQLAlchemy
from app import db

class Datatable(db.Model):
    dataid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    NCT_number = db.Column(db.String(255), unique = True)
    Status = db.Column(db.String(255))
    Study_title = db.Column(db.String(1024))
    Condition = db.Column(db.String(1024))
    Intervention = db.Column(db.String(1024))
    Location = db.Column(db.String(1024))

    def __init__(self, NCT_number, Status, Study_title, Condition, Intervention, Location):
        self.NCT_number = NCT_number
        self.Status = Status
        self.Study_title = Study_title
        self.Condition = Condition
        self.Intervention = Intervention
        self.Location = Location  
