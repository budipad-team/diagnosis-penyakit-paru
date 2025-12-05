# Pulmo Expert System

Aplikasi sistem pakar diagnosis penyakit paru berbasis web menggunakan Flask. Aplikasi ini membantu mendeteksi penyakit paru secara dini berdasarkan gejala yang dipilih oleh pengguna.

## 🚀 Cara Menjalankan Aplikasi
```bash
cd "diagnosis-penyakit-paru"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py


➡ Setelah berjalan, buka di browser:
http://127.0.0.1:5000/
```

## 🧠 Teknologi
- Python
- Flask (Web Framework)
- HTML, CSS (Tampilan)
- JSON (Basis aturan/knowledge base)

## 📂 Struktur Project
- app.py → main program
- sistem_pakar.py → engine sistem pakar
- knowledge_base.json → aturan penyakit & gejala
- visitor_data.csv → data pengunjung
- templates/ → file HTML
- static/ → CSS & gambar

## 🎯 Tujuan
Membantu deteksi awal penyakit paru sehingga masyarakat dapat mengambil langkah medis tepat waktu.

---

**Made with ❤️ by budipad Team**
