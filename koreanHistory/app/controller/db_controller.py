from flask import Blueprint, jsonify, request
from app.service.db_service import DBService

db_service = DBService()
db_bp = Blueprint("DBController", __name__)

@db_bp.route('/incident')
def all_incident():
    incidents = db_service.get_all_title()
    return jsonify(incidents)


@db_bp.route('/getdata', methods=['POST'])
def getdata():
    param = request.get_json()  # 요청 Body를 JSON형식으로 해석
    print("================param=======================")
    print(param)
    
    
    return jsonify({"key": "values"})
    