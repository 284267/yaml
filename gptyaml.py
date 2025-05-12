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
    app.run(host='0.0.0.0', port=5000, debug=True)


