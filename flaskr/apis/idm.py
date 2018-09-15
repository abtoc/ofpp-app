from datetime import datetime
from flask import Blueprint, jsonify
from flaskr.models import Person
from flaskr.services.worklogs import WorkLogService
from flaskr import app, db, auth

bp = Blueprint('api_idm', __name__, url_prefix='/api/idm')

@bp.route('/<idm>', methods=['GET'])
@auth.login_required
def get(idm):
    person = Person.query.filter(Person.idm == idm).first()
    if person is None:
        return jsonify({ 'name': '該当者無し'}), 404
    result = dict(
        name=person.display_or_name
    )
    return jsonify(result), 200

@bp.route('/<idm>', methods=['POST'])
@auth.login_required
def post(idm):
    person = Person.query.filter(Person.idm == idm).first()
    if person is None:
        return jsonify({ 'name': '該当者無し'}), 404
    now = datetime.now()
    yymm = now.strftime('%Y%m')
    dd = now.day
    worklog = WorkLogService.get_or_new(person.id, yymm, dd)
    try:
        worklog.update_api(now)
    except Exception as e:
        db.session.rollback()
        app.logger.exception(e)
        return jsonify({'message': str(e)}), 500
    if bool(worklog.work_out):
        result = dict(
            work_in = worklog.work_in,
            work_out = worklog.work_out
        )
    else:
        result = dict(
            work_in = worklog.work_in,
            work_out = '--:--'
        )        
    return jsonify(result), 200

@bp.route('/<idm>', methods=['DELETE'])
@auth.login_required
def delete(idm):
    return jsonify({}), 200
