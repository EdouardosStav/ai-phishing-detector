from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
from backend.core.heurestics import analyze_url, calculate_score, classify_risk
from backend.core.gpt_summary import generate_gpt_summary
from backend.core.pdf_generator import generate_pdf_report, generate_email_pdf_report
from backend.core.email_analysis import analyze_email_text, calculate_email_score

load_dotenv()
app = Flask(__name__)
CORS(app)

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


@app.route('/analyze-email', methods=['POST'])
def analyze_email():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Missing email'}), 400

    indicators = analyze_email_text(email)
    score = calculate_email_score(indicators)
    risk_level = classify_risk(score)

    return jsonify({
        'email': email,
        'score': score,
        'risk_level': risk_level,
        'indicators': indicators
    })

@app.route('/generate-email-report', methods=['POST'])
def generate_email_report():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Missing email'}), 400

    indicators = analyze_email_text(email)
    score = calculate_email_score(indicators)
    risk_level = classify_risk(score)
    gpt_summary = generate_gpt_summary(email, indicators, risk_level)
    output_path = generate_email_pdf_report(email, indicators, score, risk_level, gpt_summary)

    response = make_response(send_file(output_path, as_attachment=True, mimetype='application/pdf'))
    response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
    return response

if __name__ == '__main__':
    app.run(debug=True)
