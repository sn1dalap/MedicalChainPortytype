from flask import Flask, render_template, request, redirect, url_for 
from blockchain import Blockchain, Block
from encryption import Encryption
from database import init_db, add_patient, get_patient_block_index
from datetime import datetime

# Инициализация Flask-приложения
app = Flask(__name__)

# Инициализация блокчейна и шифрования
blockchain = Blockchain()
encryption = Encryption()

# Инициализация базы данных
init_db()

# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        # Создаем новый блок для пациента
        new_block = Block(len(blockchain.chain), blockchain.get_latest_block().hash, datetime.now(), f"Patient: {name}")
        blockchain.add_block(new_block)
        # Добавляем пациента в базу данных
        add_patient(name, new_block.index)
        return redirect(url_for('login'))
    return render_template('register.html')

# Маршрут для входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        block_index = get_patient_block_index(name)
        if block_index is not None:
            return redirect(url_for('patient', name=name))
        else:
            return "Пациент не найден"
    return render_template('login.html')

# Маршрут для страницы пациента
@app.route('/patient/<name>')
def patient(name):
    block_index = get_patient_block_index(name)
    if block_index is not None:
        block = blockchain.chain[block_index]
        return render_template('patient.html', name=name, block=block)
    return "Пациент не найден"

# Маршрут для страницы врача
@app.route('/doctor')
def doctor():
    return render_template('doctor.html')

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)