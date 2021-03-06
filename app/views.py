#!bin/python

from flask import render_template, request, jsonify, session, redirect
from app import app, db, models
import config
import datetime
import json
import pdb
import twilio.twiml
from twilio.rest import TwilioRestClient

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


#Main page
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@app.route('/register', methods=['GET'])
@app.route('/login', methods=['GET'])
def index():
    return render_template('splash.html')

#Volunteer signup form
@app.route('/volunteer/new', methods=['POST'])
def new_vol():
    data = request.get_json()
    app.logger.info(data)
    vol = models.Vol(
        email=data['email'],
        phone=data['phone'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        linkedin=(data['linkedin'] if 'linkedin' in data else None),
        facebook=(data['facebook'] if 'facebook' in data else None),
        occupation=data['occupation'],
        accepts_texts=(True if data['accepts_texts'].lower() == 'yes' else False),
        postal_code=data['postal_code'],
        created_on=datetime.datetime.utcnow(),
        mon=(True if 'monday' in data else False),
        tue=(True if 'tuesday' in data else False),
        wed=(True if 'wednesday' in data else False),
        thu=(True if 'thursday' in data else False),
        fri=(True if 'friday' in data else False),
        sat=(True if 'saturday' in data else False),
        sun=(True if 'sunday' in data else False))

    db.session.add(vol)
    db.session.commit()
    return 'Success!'

#New project form template
@app.route('/project/new', methods=['GET'])
def new_project():
    return render_template('new_project.html')

#New project form submission
@app.route('/project/new', methods=['POST'])
def save_project():

    vol_ids = request.get_json()['volunteers']
    project = request.get_json()['project']

    new_project = models.Project(
        name=project['name'],
        organization=project['organization'],
        description=project['description'],
        tools=project['tools'],
        day=project['day'],
        created_on=datetime.datetime.utcnow(),
        happens_on=datetime.datetime.utcnow() + datetime.timedelta(days=2)
    )
    db.session.add(new_project)
    db.session.commit()

    pas = [models.ProjectAssignment(project_id=new_project.id, vol_id=vol_id) for vol_id in vol_ids]
    db.session.add_all(pas)
    for vol_id in vol_ids:
        vol = models.Vol.query.get(vol_id)
        request_vol(vol, new_project)
    return 'Successfully added volunteers {} to the project {}'.format(','.join(str(vol_ids)), project['name'])

@app.route('/project/<int:project_id>', methods=['GET'])
def project(project_id):
    p = models.Project.query.get(project_id)
    return render_template('project_info.html')

@app.route('/projects', methods=['GET'])
def project_data():
    out = {"projects":[]}
    for project in models.Project.query.all():
        pd = project.as_dict()
        pd['vols'] = [vol.as_dict() for vol in project.vols]
        out['projects'].append(pd)
    return jsonify(out)

@app.route('/volunteer', methods=['GET'])
def get_vols_list():
    vols = models.Vol.query.all()
    jvols = jsonify({'volunteers':[vol.as_dict() for vol in vols]})
    return jvols

@app.route('/volunteers', methods=['GET'])
def list_vols():
    return render_template('vols_list.html')

@app.route('/volunteers/new', methods=['GET'])
def vols_new():
    return render_template('vol_sign_up.html')
    
@app.route('/project_assignment_confirmation', methods=['POST'])
def confirm():
    app.logger.info(request.values)
    from_number = request.values.get('From')[2:]
    vol = db.session.query(models.Vol).filter_by(phone=from_number).first()
    pa = db.session.query(models.ProjectAssignment).filter_by(vol_id=vol.id).first()
    resp = twilio.twiml.Response()
    if pa:
        body = request.values.get('Body')
        if body.lower() == 'yes':
            pa.request_accepted = True
            db.session.commit()
            resp.message('Your participation is confirmed.\nThank you!')
        elif body.lower() == 'no':
            pa.request_accepted = False
            db.session.commit()
            resp.message('Thank you! We will notify you about upcoming opportunities.')
        else:
            resp.message("Please reply 'Yes' to confirm or 'No' to reject")
    return str(resp)

#Sends request to the volunteer and stores the state in the DB
def request_vol(vol, project):

    client = TwilioRestClient(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
    body = "Hi {},\n {} would need your help on {}\n{}\n\n"\
        .format(vol.first_name,
                project.organization,
                project.day,
                project.description)
    body += "Please reply 'Yes' to confirm participation or 'No' to reject."
    #Send SMS
    client.messages.create(to=vol.phone,
                                     from_=config.TWILIO_SENDER_NUMBER,
                                     body=body)
    #Store state
    pa = db.session.query(models.ProjectAssignment).filter_by(vol_id=vol.id, project_id=project.id).first()
    pa.request_sent = True
    db.session.commit()
