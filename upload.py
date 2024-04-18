from flask import Blueprint, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

upload_bp = Blueprint('upload_bp', __name__)

ALLOWED_EXTENSIONS = {'mp3', 'wav'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    bpm_adjustment = request.form.get('bpmAdjustment')
    if 'file1' not in request.files or 'file2' not in request.files:
        flash('No file part')
        return redirect(request.url)
        flash('No file part')
        return redirect(request.url)
    file1 = request.files['file1']
    file2 = request.files['file2']
    if file1.filename == '' or file2.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        filepath1 = os.path.join('uploads', filename1)
        filepath2 = os.path.join('uploads', filename2)
        file1.save(filepath1)
        file2.save(filepath2)
        from process_audio import extract_vocals, extract_instruments, combine_audio
        vocals_path = extract_vocals(filepath1)
        instruments_path = extract_instruments(filepath2)
        combined_song_path = combine_audio(vocals_path, instruments_path)
        return redirect(url_for('download_bp.download_file', filename='combined_song.mp3'))
        return redirect(url_for('download_file', filename='combined_song.mp3'))
    else:
        flash('Allowed file types are mp3, wav')
        return redirect(request.url)