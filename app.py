import requests
import re
from flask import Flask, redirect, Response

app = Flask(__name__)

def get_ok_ru_link(video_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://ok.ru/"
    }
    try:
        # الدخول لصفحة الفيديو في OK.ru
        url = f"https://ok.ru/video/{video_id}"
        response = requests.get(url, headers=headers, timeout=10).text
        
        # البحث عن رابط الـ metadata المشفر في الصفحة
        metadata_url = re.search(r'data-module="OKVideo".*?data-options="(.*?)"', response)
        if metadata_url:
            import html
            import json
            options = json.loads(html.unescape(metadata_url.group(1)))
            metadata = json.loads(options['flashvars']['metadata'])
            
            # جلب رابط m3u8 (HLS)
            m3u8_url = metadata.get('hlsManifestUrl')
            return m3u8_url
    except Exception as e:
        print(f"Error: {e}")
    return None

@app.route('/play/<video_id>')
def play(video_id):
    # تنظيف المعرف من .m3u8
    v_id = video_id.split('.')[0]
    link = get_ok_ru_link(v_id)
    
    if link:
        # إعادة التوجيه للرابط المباشر
        return redirect(link)
    return "Video Not Found", 404

@app.route('/')
def home():
    return "OK.ru Proxy is Active"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
