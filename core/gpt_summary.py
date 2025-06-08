import os
import openai

def generate_gpt_prompt(url, indicators, risk_level):
    active_indicators = [k.replace("_", " ") for k, v in indicators.items() if v and k != "suspicious_keywords"]
    keyword_list = indicators.get("suspicious_keywords", [])
    indicator_text = ", ".join(active_indicators)
    keyword_text = ", ".join(keyword_list) if keyword_list else "none"

    return (
        f"The following URL has been analyzed for phishing risk: {url}\n"
        f"Risk Level: {risk_level}\n"
        f"Triggered Heuristics: {indicator_text}\n"
        f"Suspicious Keywords Found: {keyword_text}\n\n"
        "Please write a short, clear explanation (like for a security report) on why this URL is risky. "
        "Focus on clarity, no fluff."
    )

def generate_gpt_summary(url, indicators, risk_level):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        return "No API key found. Cannot generate GPT summary."

    prompt = generate_gpt_prompt(url, indicators, risk_level)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a cybersecurity analyst helping write threat reports."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=300
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error generating GPT summary: {str(e)}"