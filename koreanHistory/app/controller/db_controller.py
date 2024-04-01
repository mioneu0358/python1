from flask import Blueprint, jsonify, request
from app.service.db_service import DBService

db_service = DBService()
db_bp = Blueprint("DBController", __name__)

# @db_bp.route('/incident')
# def all_incident():
#     incidents = db_service.get_all_title()
#     return jsonify(incidents)

@db_bp.route('/getdata/category', methods=['POST'])
def getdata():
    rq = request.get_json()

    king = "%" + rq['king'].strip() + "%"
    year = rq['year']
    content = "%" + rq['content'].strip() + "%"
    
    result = db_service.get_incident(king,year,content)
    print(f"result:{result}")
    
    return jsonify(result)
    