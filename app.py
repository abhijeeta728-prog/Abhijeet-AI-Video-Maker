from flask import Flask, render_template, request, jsonify
import os
import requests

# सटीक डायरेक्टरी पाथ सेट करना ताकि TemplateNotFound कभी न आए
current_dir = os.path.abspath(os.path.dirname(__file__))
templates_dir = os.path.join(current_dir, 'templates')

app = Flask(__name__, template_folder=templates_dir)

DEFAULT_CONFIG = {
    "bg_color": "#1a1a1a",
    "box_width": "450",
    "accent_color": "#ff6600",
    "app_status": "active"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-config', methods=['GET'])
def get_config():
    config = {
        "bg_color": os.environ.get("APP_BG_COLOR", DEFAULT_CONFIG["bg_color"]),
        "box_width": os.environ.get("APP_BOX_WIDTH", DEFAULT_CONFIG["box_width"]),
        "accent_color": os.environ.get("APP_ACCENT_COLOR", DEFAULT_CONFIG["accent_color"]),
        "app_status": os.environ.get("APP_STATUS", DEFAULT_CONFIG["app_status"])
    }
    return jsonify({"success": True, "data": config})

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json or {}
    topic = data.get('topic')
    length = data.get('length', 30)
    voice = data.get('voice', 'male')
    style = data.get('style', 'realistic')

    if not topic:
        return jsonify({"success": False, "error": "विषय (Topic) लिखना अनिवार्य है!"})

    GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

    if not GEMINI_KEY:
        return jsonify({"success": False, "error": "Google API Key सर्वर पर सेट नहीं है!"})

    try:
        gemini_url = f"https://googleapis.com{GEMINI_KEY}"
        payload = {
            "contents": [{"parts": [{"text": f"Write a short, engaging video script in Hindi about: {topic}. Keep it suitable for a {length} seconds video."}]}]
        }
        
        gemini_res = requests.post(gemini_url, json=payload)
        script_text = "AI Story Generated"
        if gemini_res.status_code == 200:
            res_data = gemini_res.json()
            try:
                script_text = res_data['candidates'][0]['content']['parts'][0]['text']
            except:
                pass

        formatted_prompt = topic.replace(" ", "_")
        free_video_url = f"https://pollinations.ai{formatted_prompt}_{style}?width=360&height=640&enhance=true&feed=true"
        
        return jsonify({
            "success": True, 
            "video_url": free_video_url,
            "script": script_text
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
    
