from flask import render_template, request, jsonify, session, redirect
from app import app, db, models
import datetime
import twilio.twiml


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('volunteer.html')

@app.route('/ngo', methods=['GET'])
def ngo():
    return render_template('ngo.html')

@app.route('/volunteer/new', methods=['POST'])
def new_vol():
    data = request.get_json()
    app.logger.info(data)
    # vol = models.Vol()
    # db.session.add(vol)
    # db.session.commit()
    return str(data)

@app.route('/project/new', methods=['GET','POST'])
def new_project():
    np = models.Project(created_on=datetime.datetime.utcnow())
    db.session.add(np)
    db.session.commit()
    return redirect('/project/%s' % np.id)

@app.route('/project/<int:project_id>', methods=['GET'])
def project(project_id):
    p = models.Project.query.get(project_id)
    if not p.updated_on:
        return render_template('new_project_form.html')
    else:
        return render_template('project_info.html')






@app.route('/volunteer/', methods=['GET'])
def list_vols():
    vols = models.Vol.query.all()
    return jsonify([vol.__dict__ for vol in vols])


@app.route('/request_vols', methods=['POST'])
#For each vol id,
def request_vols():
    vols = request.get_json()

#     for vol_id in vols:
#         send
#
#
#
#
# def sms_request():
#
#     counter = session.get('counter', 0)
#
#     # increment the counter
#     counter += 1
#
#     # Save the new counter value in the session
#     session['counter'] = counter
#
#     from_number = request.values.get('From')
#     if from_number in callers:
#         name = callers[from_number]
#     else:
#         name = "Monkey"
#
#     message = "".join([name, " has messaged ", request.values.get('To'), " ",
#         str(counter), " times."])
#     resp = twilio.twiml.Response()
#     resp.sms(message)
#
#     return str(resp)
