from app import db

class Vol(db.Model):
    __tablename__ = 'Vol'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), unique=True)
    last_name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    phone =  db.Column(db.String(120), unique=True)
    occupation = db.Column(db.String(120))
    postal_code = db.Column(db.Integer)
    linkedin = db.Column(db.String(120))
    facebook = db.Column(db.String(120))
    is_disabled = db.Column(db.Boolean)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    mon = db.Column(db.Boolean)
    tue = db.Column(db.Boolean)
    wed = db.Column(db.Boolean)
    thu = db.Column(db.Boolean)
    fri = db.Column(db.Boolean)
    sat = db.Column(db.Boolean)
    sun = db.Column(db.Boolean)