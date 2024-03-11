from flask import Blueprint, jsonify, request
from app.service.db_service import DBService

db_service = DBService()
db_bp = Blueprint("DBController", __name__)

@db_bp.route('/incident')
def all_incident():
    incidents = db_service.get_all_title()
    return jsonify(incidents)


