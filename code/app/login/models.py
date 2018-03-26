from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    userid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique = True)
    password = db.Column(db.String(255))
    image = db.Column(db.String(255))
    phone_no = db.Column(db.String(24))

    def __init__(self, name, email, password, image, phone_no):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.image = image
        self.phone_no = phone_no

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return '<logged in as %r>' % self.email
