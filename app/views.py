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