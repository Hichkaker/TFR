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


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@app.route('/register', methods=['GET'])
@app.route('/login', methods=['GET'])
def index():
    return render_template('vol_sign_up.html')


@app.route('/volunteer/new', methods=['POST'])
def new_vol():
    data = request.get_json()
    app.logger.info(data)
    vol = models.Vol(
        email=data['email'],
        phone=data['phone'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        linkedin=data['linkedin'],
        facebook=data['facebook'],
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
    return redirect('/volunteers')

@app.route('/project/new', methods=['GET'])
def new_project():
    return render_template('new_project.html')

@app.route('/project/new', methods=['POST'])
def save_project():

    vol_ids = request.get_json()['volunteers']
    project = request.get_json()['project']

    new_project = models.Project(
        name=project['name'],
        organization=project['organization'],
        description=project['description'],
        tools=project['tools'],
        day=project['day']
    )
    db.session.add(new_project)
    db.session.commit()

    pas = [models.ProjectAssignment(project_id=new_project.id, vol_id=vol_id) for vol_id in vol_ids]
    db.session.add_all(pas)
    for vol_id in vol_ids:
        vol = models.Vol.query.get(vol_id)
        request_vol(vol, new_project)
    return 'Success'





@app.route('/project/<int:project_id>', methods=['GET'])
def project(project_id):
    p = models.Project.query.get(project_id)
    return render_template('project_info.html')

@app.route('/project/<int:project_id>/data', methods=['GET'])
def project_data(project_id):
    p = models.Project.query.get(project_id)
    return str(p)


# @app.route('/project/<int:project_id>/volunteers', methods=['GET'])
@app.route('/volunteer', methods=['GET'])
def get_vols_list():
    vols = models.Vol.query.all()
    jvols = jsonify({'volunteers':[vol.as_dict() for vol in vols]})
    return jvols

@app.route('/volunteers', methods=['GET'])
def list_vols():
    return render_template('vols_list.html')


@app.route('/project_assignment_confirmation', methods=['POST'])
def confirm():
    app.logger.info(request.values)
    from_number = request.values.get('From')
    vol = db.session.query(models.Vol.filter_by(phone=from_number)).first()
    pa = db.session.query(models.ProjectAssignment).filter_by(vol_id=vol.id).first()
    resp = twilio.twiml.Response()
    if pa:
        body = request.values.get('Body')
        if body == '1':
            pa.request_accepted = True
            db.session.commit()
            resp.sms('Your participation is confirmed.\nThank you!')
        if body == '0':
            pa.request_accepted = False
            db.session.commit()
            resp.sms('Maybe other time!\nThank you!')
        else:
            resp.sms('Please reply "1" to confirm or "0" to reject')

def request_vol(vol, project):

    client = TwilioRestClient(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
    body = "Hi {},\n {} would need your help on {}\n{}\n"\
        .format(vol.first_name,
                project.organization,
                project.day,
                project.description)
    body += "If you can help, please reply '1', if not reply '0'"

    #Send SMS
    message = client.messages.create(to=vol.phone, from_=config.TWILIO_SENDER_NUMBER,
                                     body=body)
    #Store state
    pa = db.session.query(models.ProjectAssignment).filter_by(vol_id=vol.id, project_id=project.id).first()
    pa.request_sent = True
    db.session.commit()