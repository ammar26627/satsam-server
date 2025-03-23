from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin

embeddings_bp = Blueprint('get_embeddings', __name__)

@embeddings_bp.route('/get_embeddings', methods=['POST'])
@cross_origin()
def get_embeddings():
    id = request.form.get('ID')
    queue_manager = current_app.config['QUEUE_MANAGER']
    if id in queue_manager.job_results:
        response = queue_manager.job_results[id]
        status = 200
        queue_manager.job_results.pop(id)
    else:
        queue_size = queue_manager.request_queue.qsize()
        estimated_time = (queue_size+1) * 5000
        response = {
            'job_id': id,
            'timeout': estimated_time
        }
        status = 202

    return jsonify(response), status

