import os
import tempfile
import openai
from flask import Blueprint, render_template, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
from app.utils.file_handling import schedule_file_deletion
from app.utils.audio_handling import load_audio
from langchain.text_splitter import RecursiveCharacterTextSplitter


callnotesgenerator_bp = Blueprint('callnotesgenerator', __name__)

@callnotesgenerator_bp.route('/callnotesgenerator')
def callnotesgenerator():
    return render_template('callnotesgenerator.html')


@callnotesgenerator_bp.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    audio_file = request.files['file']

    # Save the file temporarily
    _, file_ext = os.path.splitext(secure_filename(audio_file.filename))
    temp_file = tempfile.NamedTemporaryFile(suffix=file_ext, delete=False)
    audio_file.save(temp_file.name)

    # print(f"file is, {temp_file.name}")
    temp_wav_file = os.path.join( current_app.config['UPLOAD_FOLDER'], "test_audio.wav")
    # print(f"temp_wav_file in route is, {temp_wav_file}")

    # Get transcript text
    transcript_text = load_audio(temp_file.name,temp_wav_file)

    # Close and delete the temporary file
    temp_file.close()
    os.unlink(temp_file.name)

    # Save the transcript as a text file
    transcript_file = secure_filename(audio_file.filename) + ".txt"
    transcript_path = os.path.join(current_app.config['UPLOAD_FOLDER'], transcript_file)

    with open(transcript_path, "w") as f:
        f.write(transcript_text)

    return jsonify({'transcript_file': transcript_file, 'transcript_text': transcript_text})

@callnotesgenerator_bp.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_from_directory(directory=current_app.config['UPLOAD_FOLDER'], filename=filename, as_attachment=True)



@callnotesgenerator_bp.route('/summarize', methods=['POST'])
def summarize_route():
    data = request.get_json()
    transcript = data.get('transcript')
    summary = summarize(transcript)
    return jsonify({'summary': summary})


def summarize(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200)
    texts = text_splitter.split_text(text)
    summaries = []
    for t in texts:
        summary = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are very good at putting together meeting notes / memos / summary of an article"},
                {"role": "user", "content": f"Please put together a summary of the following call transcript / meeting notes / article: {t}."},
            ],
            temperature=0.3,
            max_tokens=120,
        )
        summaries.append(summary.choices[0].message.content)
    return " ".join(s for s in summaries)


@callnotesgenerator_bp.route('/delete_file', methods=['POST'])
def delete_file_route():
    data = request.get_json()
    filename = data.get('filename')

    if not filename:
        return jsonify({'error': 'No filename provided'}), 400

    delay = 3000  # Delay in seconds (e.g., 300 seconds = 5 minutes)
    schedule_file_deletion(filename, delay)

    return jsonify({'message': f'File scheduled for deletion in {delay} seconds'})