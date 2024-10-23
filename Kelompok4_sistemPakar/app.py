from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL Database Configuration
db_config = {
    'host': 'localhost',
    'port': '3306',
    'user': 'root',
    'password': 'Tanaman123%',
    'database': 'simpak'
}

# Function to connect to MySQL database
def connect_db():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id_gejala, symptom_name FROM gejala")
    gejala_list = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', gejala_list=gejala_list)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        selected_gejala = request.form.getlist('gejala')  # Ambil data gejala yang dipilih pengguna
        
        # Proses gejala yang dipilih dari database
        conn = connect_db()
        cursor = conn.cursor()
        total_bobot = 0
        
        for gejala_id in selected_gejala:
            cursor.execute("SELECT cf_expert FROM certainty_factors WHERE id_gejala = %s", (gejala_id,))
            result = cursor.fetchone()
            if result:  # Check if result is not None
                cf_expert = result[0]
                total_bobot += cf_expert
        
        conn.close()
        
        return render_template('result.html', total_bobot=total_bobot)

if __name__ == '__main__':
    app.run(debug=True)
