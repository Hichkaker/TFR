from flask import render_template, request, jsonify
from app import app, db, models


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/volunteer/new', methods=['POST'])
def new_vol():
    data = request.get_json()
    app.logger.info(data)
    # vol = models.Vol()
    # db.session.add(vol)
    # db.session.commit()
    return str(data)

@app.route('/list_vols', methods=['GET'])
def list_vols():
    vols = models.Vol.query.all()
    return jsonify([vol.__dict__ for vol in vols])

@app.route('/request_vols', methods=['GET'])
def request_vols():
    vols = request.get_json()

#
#
# import twilio.twiml
#
# # The session object makes use of a secret key.
# SECRET_KEY = 'a secret key'
# app = Flask(__name__)
# app.config.from_object(__name__)
#
# # Try adding your own number to this list!
# callers = {
#     "+14158675309": "Curious George",
#     "+14158675310": "Boots",
#     "+14158675311": "Virgil",
# }
#
# @app.route("/", methods=['GET', 'POST'])
# def hello_monkey():
#     """Respond with the number of text messages sent between two parties."""
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

if __name__ == "__main__":
    app.run(debug=True)