from flask import Blueprint
from flask_app.routes.set_image import image_bp
from flask_app.routes.get_embeddings import embeddings_bp
from flask_app.routes.test import test_bp

main_bp = Blueprint("main", __name__)

main_bp.register_blueprint(image_bp)
main_bp.register_blueprint(embeddings_bp)
main_bp.register_blueprint(test_bp)
