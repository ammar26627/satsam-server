from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
import numpy as np
from PIL import Image

image_bp = Blueprint('set_image', __name__)

@image_bp.route('/set_image', methods=['POST'])
@cross_origin() #remove
def get_embeddings():
    req_image = request.files['image']
    image = Image.open(req_image).convert('RGB')
    image_array = np.array(image)
    
    queue_manager = current_app.config['QUEUE_MANAGER']
    job_id, estimate_timeout = queue_manager.add_request_to_queue(image_array)

    return jsonify({
        'job_id': job_id,
        'timeout': estimate_timeout
    }), 202
