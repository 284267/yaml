import os
import subprocess
import time
import requests
import pyperclip
import random
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash

app = Flask(__name__)
app.secret_key = 'supersecret'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'yaml', 'yml'}
ADMIN_PASS = 'admin'
GUEST_PASS = '123456'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASS:
            session['role'] = 'admin'
            return redirect(url_for('admin_panel'))
        elif password == GUEST_PASS:
            session['role'] = 'guest'
            return redirect(url_for('guest_panel'))
        else:
            flash('密码错误！')
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('请上传文件！')
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            flash('✅ 文件上传成功！')
        else:
            flash('只能上传 .yaml 或 .yml 文件！')

    files = os.listdir(UPLOAD_FOLDER)
    return render_template('admin.html', files=files)

@app.route('/guest')
def guest_panel():
    if session.get('role') != 'guest':
        return redirect(url_for('login'))
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('guest.html', files=files)

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/delete/<filename>')
def delete_file(filename):
    if session.get('role') == 'admin':
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            flash(f'{filename} 已删除！')
    return redirect(url_for('admin_panel'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        ngrok_path = 'C:\\ngrok\\ngrok.exe'  # 替换为你自己的路径
        try:
            # 启动 ngrok 静默
            subprocess.Popen(
                [ngrok_path, 'http', '5000'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(2)

            # 获取公网地址
            tunnel_info = requests.get('http://127.0.0.1:4040/api/tunnels').json()
            public_url = tunnel_info['tunnels'][0]['public_url']

            # 生成自定义 is.gd 短链
            suffix = f"ChatGPT{random.randint(1000, 9999)}"
            short_url_req = requests.get(
                f'https://is.gd/create.php?format=simple&url={public_url}&shorturl={suffix}'
            )

            if "Error" in short_url_req.text:
                short_url = public_url
                print("⚠️ 自定义短链失败，已使用原始地址")
            else:
                short_url = short_url_req.text

            # 输出并复制
            pyperclip.copy(short_url)
            print(f"\n✅ 本地地址：http://127.0.0.1:5000")
            print(f"🌍 公网地址：{public_url}")
            print(f"🔗 自定义短链：https://is.gd/{suffix}")
            print("📋 短链已复制到剪贴板，直接 Ctrl+V 粘贴发人就行啦！\n")

        except Exception as e:
            print("❌ 启动 ngrok 或生成短链失败：", e)

    app.run(host='0.0.0.0', port=5000, debug=True)
