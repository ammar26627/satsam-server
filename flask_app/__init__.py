from flask import Flask, Blueprint
from flask_cors import CORS
import os, sys, torch, threading
from flask_app.routes import main_bp as bp
from flask_app.queue_manager import QueueManager

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config['CORS_HEADERS'] = 'Content-Type'

    app.config['QUEUE_MANAGER'] = QueueManager()

    app.register_blueprint(bp)
    return app