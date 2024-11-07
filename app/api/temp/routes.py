from . import temp_bp
from flask import jsonify, request


@temp_bp.route('/posts', methods=['GET'])
def get_posts():

    return 200
