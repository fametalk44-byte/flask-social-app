from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2, smtplib, random
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"   # session के लिए जरूरी

# Database connection function
def get_db_connection():
    return psycopg2.connect(
        dbname="socialdb",
        user="postgres",
        password="newpassword",
        host="localhost",
        port="5432"
    )

# Database setup
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        phone VARCHAR(20) NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        verified BOOLEAN DEFAULT FALSE
                    )''')
    conn.commit()
    cursor.close()
    conn.close()

init_db()

# Gmail OTP function
def send_otp(email):
    otp = str(random.randint(100000, 999999))
    session['otp'] = otp
    session['email'] = email

    sender = "gs5747173@gmail.com"
    password = "khchgeuepofesqul"   # Gmail App Password

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, email, f"Subject: Your OTP\n\nYour OTP is {otp}")
    server.quit()
    return otp

@app.route('/')
def home():
    return redirect(url_for('signup'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')

        if not (name and email and phone and password):
            return "❌ Please fill all fields!"

        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, phone, password, verified) VALUES (%s, %s, %s, %s, %s)",
                           (name, email, phone, hashed_password, False))
            conn.commit()
            cursor.close()
            conn.close()

            # Send OTP to Gmail
            send_otp(email)
            return redirect(url_for('verify'))
        except Exception as e:
            return f"⚠️ Error: {e}"
    return render_template('signup.html')

@app.route('/verify', methods=['GET','POST'])
def verify():
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        if entered_otp == session.get('otp'):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET verified=TRUE WHERE email=%s", (session['email'],))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
        else:
            return "❌ Invalid OTP!"
    return render_template('verify.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user[4], password):
            if user[5]:  # verified check
                return render_template('welcome.html', name=user[1], email=user[2], phone=user[3])
            else:
                return "⚠️ Please verify your account first!"
        else:
            return "❌ Invalid credentials!"
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(debug=True)
