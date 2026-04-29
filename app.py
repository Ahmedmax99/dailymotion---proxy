from flask import Flask, Response, redirect
import requests
import re

app = Flask(__name__)

def get_dm_m3u8(video_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        # الدخول لصفحة الفيديو لجلب بيانات البث
        url = f"https://www.dailymotion.com/player/metadata/video/{video_id}"
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        # استخراج رابط m3u8 من البيانات
        m3u8_url = data.get('qualities', {}).get('auto', [{}])[0].get('url')
        return m3u8_url
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/play/<video_id>')
def play(video_id):
    # تنظيف المعرف من .m3u8 إذا وجدت
    v_id = video_id.replace('.m3u8', '')
    real_link = get_dm_m3u8(v_id)
    
    if real_link:
        # إعادة التوجيه للرابط الحقيقي
        return redirect(real_link)
    return "Video Not Found", 404

@app.route('/')
def home():
    return "Server is Live"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
    try:
        resp = requests.get(real_m3u8_url, timeout=10)
        # نقوم بإرسال المحتوى مع الترويسة الصحيحة (Content-Type)
        return Response(resp.content, mimetype='application/vnd.apple.mpegurl')
    except Exception as e:
        return f"Error proxying content: {e}", 500

@app.route('/')
def index():
    return "Dailymotion Proxy is Running."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
