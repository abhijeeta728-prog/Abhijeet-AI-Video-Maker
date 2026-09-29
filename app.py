from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# होम पेज लोड करने के लिए
@app.route('/')
def home():
    return render_template('index.html')

# वीडियो जनरेट करने का मुख्य लॉजिक
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    if not data:
        return jsonify({"success": False, "error": "कोई डेटा प्राप्त नहीं हुआ!"})

    topic = data.get('topic')
    length = data.get('length')
    voice = data.get('voice')
    style = data.get('style')

    if not topic:
        return jsonify({"success": False, "error": "कृपया कोई टॉपिक लिखें!"})

    try:
        # Replicate AI API का उपयोग
        API_KEY = os.environ.get("REPLICATE_API_TOKEN")
        
        if not API_KEY:
            # अगर API Key सेट नहीं है, तो टेस्टिंग के लिए डेमो वीडियो लिंक भेजेंगे
            demo_video = "https://w3schools.com"
            return jsonify({"success": True, "video_url": demo_video})
            
        headers = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt_text = f"A high quality short video, {style} style, about {topic}. Duration around {length} seconds."
        
        payload = {
            "version": "153da4a7",
            "input": {"prompt": prompt_text}
        }
        
        # क्लाउड पर रिक्वेस्ट भेजना
        response = requests.post("https://replicate.com", json=payload, headers=headers)
        res_data = response.json()
        
        video_url = res_data.get("output", [None])[0]
        
        if video_url:
            return jsonify({"success": True, "video_url": video_url})
        else:
            return jsonify({"success": False, "error": "एआई वीडियो प्रोसेस होने में समय लग रहा है या एरर आया है।"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
    
