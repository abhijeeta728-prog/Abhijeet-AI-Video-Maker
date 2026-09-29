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
    topic = data.get('topic')
    length = data.get('length')
    voice = data.get('voice')
    style = data.get('style')

    if not topic:
        return jsonify({"success": False, "error": "कृपया कोई टॉपिक लिखें!"})

    try:
        # यहाँ हम Replicate AI का उपयोग वीडियो जनरेट करने के लिए करेंगे
        # यह प्रोसेस सीधे क्लाउड पर चलेगी, जिससे मोबाइल पर कोई लोड नहीं पड़ेगा
        API_KEY = os.environ.get("REPLICATE_API_TOKEN")
        
        if not API_KEY:
            # अगर अभी API Key सेट नहीं है, तो टेस्टिंग के लिए एक डेमो वीडियो लिंक भेजेंगे
            demo_video = "https://w3schools.com"
            return jsonify({"success": True, "video_url": demo_video})
            
        headers = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json"
        }
        
        # एआई मॉडल के लिए निर्देश (प्रॉम्प्ट)
        prompt_text = f"A high quality short video, {style} style, about {topic}. Duration around {length} seconds."
        
        # Replicate पर Luma Dream Machine या Minimax वीडियो मॉडल को कॉल करना
        payload = {
            "version": "153da4a7", # एआई मॉडल का सटीक वर्जन आईडी
            "input": {"prompt": prompt_text}
        }
        
        # यहाँ क्लाउड पर वीडियो बनने की रिक्वेस्ट जाती है
        response = requests.post("https://replicate.com", json=payload, headers=headers)
        res_data = response.json()
        
        # वीडियो का फाइनल लिंक निकालना
        video_url = res_data.get("output", [None])[0]
        
        if video_url:
            return jsonify({"success": True, "video_url": video_url})
        else:
            return jsonify({"success": False, "error": "एआई वीडियो प्रोसेस होने में समय लग रहा है।"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
  
