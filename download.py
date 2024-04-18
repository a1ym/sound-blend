from flask import Blueprint, send_from_directory

download_bp = Blueprint('download_bp', __name__)

@download_bp.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(directory='output', filename=filename)