from flask import Flask, Response, request
import subprocess
import os
import requests

app = Flask(__name__)

def get_m3u8_link(video_id):
    url = f"https://www.dailymotion.com/video/{video_id}"
    try:
        result = subprocess.run(
            ["streamlink", url, "best", "--stream-url"],
            capture_output=True,
            text=True,
            check=True
        )
        m3u8_url = result.stdout.strip()
        if m3u8_url and "m3u8" in m3u8_url:
            return m3u8_url
    except Exception as e:
        print(f"Error fetching link for {video_id}: {e}")
    return None

@app.route('/play/<video_id>')
def play_video(video_id):
    # إزالة .m3u8 إذا كانت موجودة في نهاية المعرف
    video_id = video_id.replace('.m3u8', '')
    
    # جلب الرابط الحقيقي من ديلي موشن
    real_m3u8_url = get_m3u8_link(video_id)
    
    if not real_m3u8_url:
        return "Error: Could not find stream", 404

    # بدلاً من إعادة التوجيه (Redirect)، سنقوم بجلب محتوى الملف وإرساله
    # هذا يضمن أن المشغل (مثل XPlayer) يرى محتوى m3u8 حقيقي فوراً
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
