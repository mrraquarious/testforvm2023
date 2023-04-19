import openai
import os
from flask import Blueprint, render_template, request, jsonify

summarizer_bp = Blueprint('summarizer', __name__)

@summarizer_bp.route('/summarizer')
def summarizer():
    return render_template('summarizer.html')

@summarizer_bp.route('/summarizer/summarize', methods=['POST'])
def summarize_route():
    text = request.json['text']
    summary = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are very good at putting together summary of a news article and giving the article a proper title"},
            {"role": "user", "content": f"Please put together a summary of the following article in 130 words, and give it a title in the first line: {text}."},
        ],
        temperature=0.3,
        max_tokens=150,
    )
    return summary.choices[0].message.content

@summarizer_bp.route('/summarizer/translate', methods=['POST'])
def translate():
    text = request.json['text']
    summary = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional translator"},
            {"role": "user", "content": f"Please translate the following text into Simplified Chinese: {text}."},
        ],
        temperature=0.3,
    )
    return summary.choices[0].message.content 