from flask import Blueprint, send_file, jsonify, request

page_bp = Blueprint('PageController', __name__)

@page_bp.route('/')
def main():
    """
    메인 페이지
    :return: view/index.html
    """
    return send_file("view/index.html")

