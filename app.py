# Main application entry point for BelajarYuk
from flask import Flask, render_template

app = Flask(__name__)

# Membuat rute untuk halaman utama
@app.route('/')
def dashboard():
    # Mengarahkan ke file index.html yang ada di dalam folder templates/dashboard/
    return render_template('dashboard/index.html')

# Menjalankan server
if __name__ == '__main__':
    # debug=True agar server otomatis restart jika ada perubahan kode
    app.run(debug=True)