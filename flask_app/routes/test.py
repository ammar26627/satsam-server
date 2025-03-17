from flask import Blueprint

test_bp = Blueprint("test", __name__)

@test_bp.route('/test', methods=['GET'])
def test():
    return 'System is up an running...'