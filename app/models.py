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
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)
    accepts_texts = db.Column(db.Boolean)
    mon = db.Column(db.Boolean)
    tue = db.Column(db.Boolean)
    wed = db.Column(db.Boolean)
    thu = db.Column(db.Boolean)
    fri = db.Column(db.Boolean)
    sat = db.Column(db.Boolean)
    sun = db.Column(db.Boolean)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Project(db.Model):
    __tablename__ = 'Project'

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)
    name = db.Column(db.String(100))
    organization = db.Column(db.String(100))
    description = db.Column(db.String(10000))
    tools = db.Column(db.String(10000))
    day = db.Column(db.String(10))
    # from_time = db.Column(db.DateTime)
    # to_time = db.Column(db.DateTime)
    vols = db.relationship('ProjectAssignment')

class ProjectAssignment(db.Model):

    __tablename__ = 'ProjectAssignment'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id))
    vol_id = db.Column(db.Integer, db.ForeignKey(Vol.id))
    request_sent = db.Column(db.Boolean)
    request_accepted = db.Column(db.Boolean)
    vol = db.relationship('Vol')




