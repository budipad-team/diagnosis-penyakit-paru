from flask import Flask, render_template, request, redirect, url_for, session, flash
import sistem_pakar as sp # Mengimpor modul sistem_pakar Anda
import os # Untuk memeriksa keberadaan file knowledge_base.json
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key_yang_sangat_aman_dan_sulit_ditebak' # Ganti dengan kunci yang kuat dan unik!

# --- Kredensial Admin (Contoh Sederhana) ---
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin" # Ganti dengan password yang lebih aman!

# --- File untuk menyimpan data pengunjung ---
VISITOR_FILE = 'visitor_data.csv'

def init_visitor_file():
    """Memastikan file CSV untuk data pengunjung ada dengan header yang sesuai."""
    if not os.path.exists(VISITOR_FILE):
        with open(VISITOR_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Nama', 'Jenis Kelamin', 'Umur', 'Berat Badan', 'Tinggi Badan', 'Riwayat Kesehatan', 'Tanggal'])

def save_visitor_data(data):
    """Menyimpan data pengunjung ke file CSV."""
    with open(VISITOR_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def get_visitor_data():
    """Mengambil semua data pengunjung dari file CSV."""
    visitors = []
    if os.path.exists(VISITOR_FILE):
        with open(VISITOR_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            for row in reader:
                if len(row) >= 7:  # Ensure row has all required fields
                    visitors.append({
                        'nama': row[0],
                        'jenis_kelamin': row[1],
                        'umur': row[2],
                        'berat_badan': row[3],
                        'tinggi_badan': row[4],
                        'riwayat_kesehatan': row[5],
                        'tanggal': row[6]
                    })
    return visitors

# --- Fungsi Utility untuk Basis Pengetahuan ---
# Pastikan basis pengetahuan dimuat dan disimpan dengan benar
def init_knowledge_base():
    """Memastikan knowledge_base.json ada dengan data default jika belum."""
    if not os.path.exists(sp.KB_FILE):
        print(f"File {sp.KB_FILE} tidak ditemukan, membuat dengan data default...")
        # Menggunakan load_knowledge_base() untuk mendapatkan default dan save_knowledge_base() untuk menyimpannya.
        sp.save_knowledge_base(sp.load_knowledge_base())


# --- Routes Autentikasi ---
@app.route('/')
def index():
    # Asumsi index.html adalah halaman diagnosis untuk pasien
    return render_template('login_choose.html')

@app.route('/login_choose')
def login_choose():
    return render_template('login_choose.html')

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in_admin'] = True
            flash('Login Admin Berhasil!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            error = "Username atau Password salah."
            flash('Username atau Password salah.', 'danger')
    return render_template('login_admin.html', error=error)

@app.route('/login_pasien', methods=['GET', 'POST'])
def login_pasien():
    error = None
    if request.method == 'POST':
        # Mengambil data dari form
        username = request.form['username']
        jenis_kelamin = request.form['jenis_kelamin']
        umur = request.form['umur']
        berat_badan = request.form['berat_badan']
        tinggi_badan = request.form['tinggi_badan']
        riwayat_kesehatan_list = request.form.getlist('riwayat_kesehatan')
        riwayat_kesehatan = ', '.join(riwayat_kesehatan_list)
        
        if username: # Cukup nama tidak kosong untuk demo
            # Simpan data pengunjung
            visitor_data = [
                username,
                jenis_kelamin,
                umur,
                berat_badan,
                tinggi_badan,
                riwayat_kesehatan,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ]
            save_visitor_data(visitor_data)
            
            session['logged_in_pasien'] = True
            session['pasien_nama'] = username
            flash(f'Selamat datang, {username}!', 'info')
            return redirect(url_for('diagnosa_pasien_ui'))
        else:
            error = "Nama pengunjung tidak boleh kosong."
            flash('Nama pengunjung tidak boleh kosong.', 'danger')
    return render_template('login_pasien.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in_admin', None)
    session.pop('logged_in_pasien', None)
    session.pop('pasien_nama', None)
    flash('Anda telah berhasil logout.', 'info')
    return redirect(url_for('index'))

# --- Routes Admin ---
@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('logged_in_admin'):
        flash('Anda harus login sebagai Admin untuk mengakses halaman ini.', 'warning')
        return redirect(url_for('login_admin'))
    
    basis_pengetahuan = sp.load_knowledge_base() # Muat basis pengetahuan dari file
    return render_template('admin_dashboard.html', basis=basis_pengetahuan)

@app.route('/admin_tambah', methods=['POST'])
def admin_tambah():
    if not session.get('logged_in_admin'):
        flash('Anda harus login sebagai Admin untuk melakukan aksi ini.', 'warning')
        return redirect(url_for('login_admin'))
    
    nama = request.form['nama']
    aturan_str = request.form['aturan']
    cf = float(request.form['cf'])
    saran = request.form['saran']

    aturan = [g.strip().lower() for g in aturan_str.split(',') if g.strip()] # Pastikan gejala lowercase dan bersih
    
    # Validasi dasar
    if not nama or not aturan or not saran or not (0.0 <= cf <= 1.0):
        flash('Input tidak valid. Pastikan semua kolom terisi dan CF antara 0.0 dan 1.0.', 'danger')
    else:
        sp.tambah_pengetahuan(nama, aturan, cf, saran)
        flash(f'Penyakit "{nama}" berhasil ditambahkan.', 'success')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin_hapus/<nama>')
def admin_hapus(nama):
    if not session.get('logged_in_admin'):
        flash('Anda harus login sebagai Admin untuk melakukan aksi ini.', 'warning')
        return redirect(url_for('login_admin'))
    
    sp.hapus_pengetahuan(nama)
    flash(f'Penyakit "{nama}" berhasil dihapus.', 'success')
    return redirect(url_for('admin_dashboard'))


# --- Routes Diagnosis Pasien ---
@app.route('/diagnosa_pasien_ui', methods=['GET', 'POST'])
def diagnosa_pasien_ui():
    if request.method == 'POST':
        gejala_terjawab = session.get('gejala_terjawab', [])
        gejala_tidak_ada = session.get('gejala_tidak_ada', [])
        jawaban = request.form.get('jawaban')
        gejala_terakhir = session.get('gejala_terakhir')
        hapus_gejala = request.form.get('hapus_gejala')
        
        if hapus_gejala:
            if hapus_gejala in gejala_terjawab:
                gejala_terjawab.remove(hapus_gejala)
                session['gejala_terjawab'] = gejala_terjawab
            return render_template('index.html', pertanyaan=gejala_terakhir, gejala_terjawab=gejala_terjawab)
        
        if jawaban == 'selesai':
            hasil_diagnosa = sp.diagnosa_step_by_step(gejala_terjawab)
            session.pop('gejala_terjawab', None)
            session.pop('gejala_tidak_ada', None)
            session.pop('gejala_terakhir', None)
            return render_template('index.html', hasil=hasil_diagnosa, gejala_terjawab=gejala_terjawab)
        
        if jawaban == 'ya' and gejala_terakhir:
            gejala_terjawab.append(gejala_terakhir)
            session['gejala_terjawab'] = gejala_terjawab
        if jawaban == 'tidak' and gejala_terakhir:
            gejala_tidak_ada.append(gejala_terakhir)
            session['gejala_tidak_ada'] = gejala_tidak_ada
        
        pertanyaan_berikutnya = sp.get_next_question(gejala_terjawab, gejala_tidak_ada)
        session['gejala_terakhir'] = pertanyaan_berikutnya
        
        if not pertanyaan_berikutnya:
            hasil_diagnosa = sp.diagnosa_step_by_step(gejala_terjawab)
            session.pop('gejala_terjawab', None)
            session.pop('gejala_tidak_ada', None)
            session.pop('gejala_terakhir', None)
            return render_template('index.html', hasil=hasil_diagnosa, gejala_terjawab=gejala_terjawab)
        
        return render_template('index.html', pertanyaan=pertanyaan_berikutnya, gejala_terjawab=gejala_terjawab)
    
    session.pop('gejala_terjawab', None)
    session.pop('gejala_tidak_ada', None)
    session.pop('gejala_terakhir', None)
    pertanyaan_pertama = sp.get_next_question([], [])
    session['gejala_terakhir'] = pertanyaan_pertama
    return render_template('index.html', pertanyaan=pertanyaan_pertama, gejala_terjawab=[])


# ... (bagian lain dari app.py) ...

@app.route('/diagnosa_admin', methods=['GET', 'POST'])
def diagnosa_admin():
    if not session.get('logged_in_admin'):
        flash('Anda harus login sebagai Admin untuk mengakses halaman ini.', 'warning')
        return redirect(url_for('login_admin'))
    
    if request.method == 'POST':
        gejala_terjawab = session.get('gejala_terjawab', [])
        gejala_tidak_ada = session.get('gejala_tidak_ada', [])
        jawaban = request.form.get('jawaban')
        gejala_terakhir = session.get('gejala_terakhir')
        hapus_gejala = request.form.get('hapus_gejala')
        
        if hapus_gejala:
            if hapus_gejala in gejala_terjawab:
                gejala_terjawab.remove(hapus_gejala)
                session['gejala_terjawab'] = gejala_terjawab
            # Render ulang dengan pertanyaan terakhir
            return render_template('diagnosa_admin.html', pertanyaan=gejala_terakhir, gejala_terjawab=gejala_terjawab)
        
        if jawaban == 'selesai':
            hasil_diagnosa = sp.diagnosa_step_by_step(gejala_terjawab)
            session.pop('gejala_terjawab', None)
            session.pop('gejala_tidak_ada', None)
            session.pop('gejala_terakhir', None)
            return render_template('diagnosa_admin.html', hasil=hasil_diagnosa, gejala_terjawab=gejala_terjawab)
        
        if jawaban == 'ya' and gejala_terakhir:
            gejala_terjawab.append(gejala_terakhir)
            session['gejala_terjawab'] = gejala_terjawab
        if jawaban == 'tidak' and gejala_terakhir:
            gejala_tidak_ada.append(gejala_terakhir)
            session['gejala_tidak_ada'] = gejala_tidak_ada
        
        pertanyaan_berikutnya = sp.get_next_question(gejala_terjawab, gejala_tidak_ada)
        session['gejala_terakhir'] = pertanyaan_berikutnya
        
        if not pertanyaan_berikutnya:
            hasil_diagnosa = sp.diagnosa_step_by_step(gejala_terjawab)
            session.pop('gejala_terjawab', None)
            session.pop('gejala_tidak_ada', None)
            session.pop('gejala_terakhir', None)
            return render_template('diagnosa_admin.html', hasil=hasil_diagnosa, gejala_terjawab=gejala_terjawab)
        
        return render_template('diagnosa_admin.html', pertanyaan=pertanyaan_berikutnya, gejala_terjawab=gejala_terjawab)
    
    session.pop('gejala_terjawab', None)
    session.pop('gejala_tidak_ada', None)
    session.pop('gejala_terakhir', None)
    pertanyaan_pertama = sp.get_next_question([], [])
    session['gejala_terakhir'] = pertanyaan_pertama
    return render_template('diagnosa_admin.html', pertanyaan=pertanyaan_pertama, gejala_terjawab=[])

@app.route('/daftar_pengunjung')
def daftar_pengunjung():
    if not session.get('logged_in_admin'):
        flash('Anda harus login sebagai Admin untuk mengakses halaman ini.', 'warning')
        return redirect(url_for('login_admin'))
    
    visitors = get_visitor_data()
    return render_template('daftar_pengunjung.html', daftar_pasien=visitors)

# ... (sisa app.py) ...

# --- Inisialisasi Aplikasi ---
if __name__ == '__main__':
    init_knowledge_base() # Pastikan basis pengetahuan ada saat aplikasi mulai
    init_visitor_file() # Pastikan file data pengunjung ada
    app.run(debug=True) # debug=True hanya untuk pengembangan