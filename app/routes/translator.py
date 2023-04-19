import openai
from flask import Blueprint, render_template, request, jsonify

translator_bp = Blueprint('translator', __name__)

@translator_bp.route('/translator')
def translator():
    return render_template('translator.html')

@translator_bp.route('/api/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text')
    source_lang = data.get('sourceLang')
    target_lang = data.get('targetLang')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional translator."},
            {"role": "user", "content": f"Translate the following text from {source_lang} to {target_lang}: {text}."},
        ],
        temperature=0.5,
    )
    return jsonify(translated_text=response.choices[0].message.content)
