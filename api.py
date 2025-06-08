from flask import Flask, request, jsonify, send_file
from core.heurestics import analyze_url, calculate_score, classify_risk
from core.gpt_summary import generate_gpt_summary
from core.pdf_generator import generate_pdf_report
import os

app = Flask(__name__)

@app.route('/analyze-url', methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    result = analyze_url(url)
    score = calculate_score(result)
    risk_level = classify_risk(score)

    return jsonify({
        'url': url,
        'score': score,
        'risk_level': risk_level,
        'indicators': result
    })

@app.route('/generate-report', methods=['POST'])
def generate_report():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    indicators = analyze_url(url)
    score = calculate_score(indicators)
    risk_level = classify_risk(score)
    summary = generate_gpt_summary(url, indicators, risk_level)
    output_path = generate_pdf_report(url, indicators, score, risk_level, summary)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
