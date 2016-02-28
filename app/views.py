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
    vols = request.get_json()['volunteers']
    project = request.get_json()['project']






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
    vols = request.get_json()
    from_number = request.values.get('From')

    vol = models.Vol.get(phone=from_number).first()
    pa = models.ProjectAssignment.get(vol_id=vol.id).first()
    if pa:
        resp = twilio.twiml.Response()
        resp.sms('Thank you!')

# Find these values at https://twilio.com/user/account


def request_vol(vol, project):
    client = TwilioRestClient(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
    body = "Hi {},\n {} would need your help from {} to {}.\n{}\n"\
        .format(vol.first_name,
                project.organization,
                project.from_time,
                project.to_time,
                project.description)
    body += "If you can help, please reply '1', if not reply '0'"

    #Send SMS
    message = client.messages.create(to=vol.phone, from_=config.TWILIO_SENDER_NUMBER,
                                     body=body)
    #Store state
    pa = models.ProjectAssignment.get(vol_id=vol.id, project_id=project.id).first()
    pa.request_sent = True
    db.session.commit()