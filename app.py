from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

GUESTBOOK_FILE = 'guestbook.json'

# 메시지 로드 함수
def load_messages():
    try:
        with open(GUESTBOOK_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# 메시지 저장 함수
def save_message(message):
    messages = load_messages()
    messages.append(message)
    with open(GUESTBOOK_FILE, 'w', encoding='utf-8') as file:
        json.dump(messages, file, ensure_ascii=False, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form['message']
        if len(message) <= 200:
            save_message(message)
            return redirect(url_for('index'))
        else:
            error = "메시지는 200자를 넘을 수 없습니다."
            return render_template('index.html', messages=load_messages(), error=error)
    
    messages = load_messages()
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
