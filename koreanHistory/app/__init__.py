from flask import Flask, send_file
from .controller.page_controller import page_bp
from .controller.db_controller import db_bp

app = Flask(__name__, static_folder="../static/resource")

app.register_blueprint(page_bp)
app.register_blueprint(db_bp, url_prefix='/db')