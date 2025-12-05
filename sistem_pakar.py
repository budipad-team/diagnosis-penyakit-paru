import json
import os

KB_FILE = 'knowledge_base.json' # Nama file untuk menyimpan basis pengetahuan

def load_knowledge_base():
    """
    Memuat basis pengetahuan dari file JSON.
    Jika file tidak ditemukan atau korup, akan membuat basis pengetahuan default.
    """
    if os.path.exists(KB_FILE):
        try:
            with open(KB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {KB_FILE} is corrupted or empty. Loading default knowledge base based on journal data.")
            default_kb = _get_default_knowledge_base()
            save_knowledge_base(default_kb)
            return default_kb
    else:
        print(f"Warning: {KB_FILE} not found. Creating and loading default knowledge base based on journal data.")
        default_kb = _get_default_knowledge_base()
        save_knowledge_base(default_kb)
        return default_kb

def _get_default_knowledge_base():
    """Mengembalikan struktur basis pengetahuan default berdasarkan data jurnal."""
    return [
        {
            "nama": "Asma",
            "aturan": ["batuk", "sesak napas", "batuk berdahak", "suara napas berbunyi ngik-ngik"],
            "cf": 0.8, # CF dipertahankan dari versi sebelumnya, tidak ada di jurnal
            "saran": "Obat yang direkomendasikan jika gejala asma muncul adalah inhaler pereda. Apabila gejala terus memburuk dan terjadi serangan asma baik secara perlahan atau secara tiba-tiba, maka pasien harus segera dirujuk ke rumah sakit. Walaupun jarang terjadi, serangan asma bisa saja merenggut nyawa."
        },
        {
            "nama": "Influenza",
            "aturan": ["batuk", "demam", "nyeri telan", "sakit kepala", "hidung tersumbat dan mengeluarkan cairan"],
            "cf": 0.7, # CF dipertahankan
            "saran": "Beberapa langkah yang bisa Anda lakukan di antaranya adalah dengan istirahat secara cukup, banyak minum, dan menjaga tubuh agar tetap hangat. Untuk menurunkan demam, mengurangi rasa sakit dan pegal disarankan untuk mengonsumsi paracetamol atau ibuprofen yang dapat dibeli bebas di apotek."
        },
        {
            "nama": "Sinusitis",
            "aturan": ["hidung tersumbat atau keluar cairan kekuningan berbau", "berkurangnya sensitivitas penciuman", "napas berbau"],
            "cf": 0.65, # CF dipertahankan
            "saran": "Sinusitis butuh waktu sekitar dua hingga tiga minggu untuk sembuh sepenuhnya. Jika menderita sinusitis ringan, obat-obatan pereda rasa sakit dan dekongestan akan membantu mengurangi gejala yang timbul. Jika gejala tidak membaik setelah seminggu, antibiotik dan steroid semprot atau tetes mungkin akan diresepkan oleh dokter."
        },
        {
            "nama": "Rhinitis",
            "aturan": ["bersin-bersin", "berkurangnya sensitivitas indera penciuman", "rasa tidak nyaman atau iritasi ringan di dalam dan area sekitar hidung"],
            "cf": 0.68, # CF dipertahankan
            "saran": "Rhinitis dapat dicegah dengan menghindari lingkungan berpolusi atau terpapar asap rokok serta alergen. Jika gejala tidak terlalu parah, perawatan rhinitis dapat dilakukan di rumah dengan mengonsumsi obat-obatan yang dijual bebas seperti dekongestan dan antihistamin. Selain itu, membersihkan saluran hidung juga dapat dilakukan. Untuk rhinitis yang tidak disebabkan oleh alergi, segera obati penyebab dasar, misalnya mengonsumsi antibiotik untuk rhinitis akibat infeksi bakteri."
        },
        {
            "nama": "Emfisema",
            "aturan": ["batuk", "batuk berdahak", "sesak napas", "batuk berlendir", "batuk berlendir diikuti keluarnya darah"],
            "cf": 0.78, # CF dipertahankan
            "saran": "Semua penderita emfisema disarankan agar menghentikan kebiasaan merokok. Untuk meringankan gejala dan memperlambat perkembangan penyakit, jenis obat-obatan yang diresepkan adalah bronchodilator, mucolytic, steroid, dan antibiotik yang disesuaikan dengan tingkat keparahan penyakit."
        },
        {
            "nama": "Bronkitis",
            "aturan": ["batuk", "batuk berdahak", "batuk berlendir", "sesak napas"],
            "cf": 0.75, # CF dipertahankan
            "saran": "Bronkitis akut biasanya akan menghilang dengan sendirinya, disarankan minum banyak cairan dan banyak istirahat. Bronkitis kronis biasanya bertahan setidaknya tiga bulan, belum ada obat yang bisa menyembuhkan, namun hindari merokok atau lingkungan perokok."
        },
        {
            "nama": "Faringitis",
            "aturan": ["batuk", "demam", "nyeri telan", "sakit kepala", "kelenjar yang membesar pada leher"],
            "cf": 0.72, # CF dipertahankan
            "saran": "Apabila gejala yang terdeteksi beresiko dan dapat menimbulkan infeksi yang lebih serius, pengobatan sakit tenggorokan pada umumnya dapat ditangani dengan menggunakan antibiotik."
        },
        {
            "nama": "Laringitis",
            "aturan": ["nyeri telan", "batuk", "demam", "sulit bicara"],
            "cf": 0.73, # CF dipertahankan
            "saran": "Disarankan untuk mengonsumsi obat-obatan pereda rasa sakit seperti ibuprofen atau parasetamol. Dianjurkan untuk banyak minum air putih, hindari minuman yang mengandung kafein dan alkohol. Menghirup inhaler yang mengandung mentol dan mengonsumsi permen mint serta berkumur-kumur dengan air garam hangat juga dianjurkan."
        },
        {
            "nama": "Tonsilitis",
            "aturan": ["batuk", "demam", "nyeri telan"],
            "cf": 0.7, # CF dipertahankan
            "saran": "Pengobatan tonsilitis biasanya diberikan untuk meringankan gejala, misalnya ibuprofen atau parasetamol sebagai pereda rasa sakit. Jika disebabkan oleh bakteri, antibiotik bisa digunakan. Pemulihan bisa ditunjang dengan istirahat yang cukup dan minum banyak cairan. Pada kasus parah dan kerap kambuh, dokter terpaksa akan melakukan operasi pengangkatan amandel."
        },
        {
            "nama": "Asbestosis",
            "aturan": ["batuk", "batuk berdahak", "batuk berlendir", "batuk berlendir diikuti keluarnya darah", "terjadi pembengkakan di area leher dan wajah", "sesak napas"],
            "cf": 0.88, # CF dipertahankan
            "saran": "Mendapatkan lebih banyak oksigen yang dibutuhkan oleh tubuh melalui paru-paru. Antibiotik bisa diberikan apabila asbestosis harus dirawat dengan jalan operasi, antibiotik dapat diberikan untuk mengurangi rasa sakit dan juga untuk mencegah terjadinya infeksi. Obat pereda sakit semacam Aspirin dan Tylenol dapat diberikan untuk mengurangi rasa sakit serta peradangan."
        },
        {
            "nama": "Tuberkulosis (TBC)",
            "aturan": ["batuk", "demam", "batuk darah"],
            "cf": 0.95, # CF dipertahankan
            "saran": "Langkah pengobatan yang dibutuhkan adalah dengan mengonsumsi beberapa jenis antibiotik dalam jangka waktu tertentu. Langkah utama untuk mencegah TB adalah dengan menerima vaksin BCG, diberikan sebelum bayi berusia 2 bulan."
        },
        {
            "nama": "Difteri",
            "aturan": ["batuk", "batuk berdahak", "sesak napas", "hidung beringus, awalnya cair, tapi lama-kelamaan menjadi kental dan kadang berdarah"],
            "cf": 0.85, # CF dipertahankan
            "saran": "Langkah pengobatan akan dilakukan dengan 2 jenis obat, yaitu antibiotik dan antitoksin. Antibiotik akan membantu tubuh untuk membunuh bakteri dan menyembuhkan infeksi. Antitoksin berfungsi untuk menetralisasi toksin atau racun difteri."
        },
        {
            "nama": "Kanker Paru-paru",
            "aturan": ["batuk", "batuk berdahak", "sesak napas", "batuk berlendir", "batuk berlendir diikuti keluarnya darah", "lelah"],
            "cf": 0.9, # CF dipertahankan
            "saran": "Operasi pengangkatan kanker bisa dilakukan jika sel kanker belum menyebar secara luas ke bagian tubuh yang lainnya. Jika kondisi kesehatan tidak memungkinkan untuk dilakukan operasi pengangkatan, proses penghancuran sel kanker dengan cara radioterapi bisa dijalankan."
        }
    ]

def save_knowledge_base(kb):
    """Menyimpan basis pengetahuan ke file JSON."""
    with open(KB_FILE, 'w', encoding='utf-8') as f:
        json.dump(kb, f, indent=4)

def diagnosa(gejala_input):
    """Melakukan diagnosis berdasarkan gejala input."""
    basis_pengetahuan = load_knowledge_base()

    hasil = []
    gejala_input_set = set(g.lower().strip() for g in gejala_input if g.strip())

    for penyakit in basis_pengetahuan:
        aturan_penyakit_set = set(a.lower().strip() for a in penyakit["aturan"] if a.strip())
        
        cocok_gejala = gejala_input_set.intersection(aturan_penyakit_set)
        
        if not aturan_penyakit_set:
            persen = 0
        else:
            persen = len(cocok_gejala) / len(aturan_penyakit_set)
            
        if persen > 0:
            cf = round(persen * penyakit["cf"], 2)
            hasil.append({
                "penyakit": penyakit["nama"],
                "cf": cf,
                "saran": penyakit["saran"],
                "gejala_tidak_ada": sorted(list(aturan_penyakit_set - gejala_input_set))
            })
    hasil = sorted(hasil, key=lambda x: x["cf"], reverse=True)
    return hasil

def tambah_pengetahuan(nama, aturan, cf, saran):
    """Menambahkan atau memperbarui entri pengetahuan baru."""
    kb = load_knowledge_base()
    aturan_bersih = [a.strip().lower() for a in aturan if a.strip()]
    
    found = False
    for p in kb:
        if p["nama"].lower() == nama.lower():
            p["aturan"] = aturan_bersih
            p["cf"] = cf
            p["saran"] = saran
            print(f"Info: Penyakit '{nama}' berhasil diperbarui.")
            found = True
            break

    if not found:
        kb.append({
            "nama": nama,
            "aturan": aturan_bersih,
            "cf": cf,
            "saran": saran
        })
        print(f"Info: Penyakit '{nama}' berhasil ditambahkan.")
    
    save_knowledge_base(kb)
    return True

def hapus_pengetahuan(nama):
    """Menghapus entri pengetahuan."""
    kb = load_knowledge_base()
    initial_len = len(kb)
    kb = [p for p in kb if p["nama"].lower() != nama.lower()]
    
    if len(kb) < initial_len:
        save_knowledge_base(kb)
        print(f"Info: Penyakit '{nama}' berhasil dihapus.")
        return True
    else:
        print(f"Warning: Penyakit '{nama}' tidak ditemukan.")
        return False

def get_all_symptoms():
    """Mengambil semua gejala unik dari basis pengetahuan."""
    kb = load_knowledge_base()
    all_symptoms = set()
    for penyakit in kb:
        for gejala in penyakit["aturan"]:
            all_symptoms.add(gejala.lower().strip())
    return sorted(list(all_symptoms))

def get_next_question(gejala_terjawab, gejala_tidak_ada=None):
    """Mendapatkan pertanyaan gejala berikutnya yang paling relevan."""
    basis_pengetahuan = load_knowledge_base()
    
    if gejala_tidak_ada is None:
        gejala_tidak_ada = []
    
    # Hitung skor relevansi untuk setiap gejala yang belum ditanyakan
    gejala_skor = {}
    for penyakit in basis_pengetahuan:
        for gejala in penyakit["aturan"]:
            # Skip gejala yang sudah dijawab (baik ya maupun tidak)
            if gejala in gejala_terjawab or gejala in gejala_tidak_ada:
                continue
                
            if gejala not in gejala_skor:
                gejala_skor[gejala] = 0
            gejala_skor[gejala] += penyakit["cf"]
    
    # Urutkan gejala berdasarkan skor relevansi
    gejala_terurut = sorted(gejala_skor.items(), key=lambda x: x[1], reverse=True)
    
    # Kembalikan gejala dengan skor tertinggi
    return gejala_terurut[0][0] if gejala_terurut else None

def diagnosa_step_by_step(gejala_terjawab):
    """Melakukan diagnosis berdasarkan gejala yang sudah dijawab."""
    basis_pengetahuan = load_knowledge_base()
    
    hasil = []
    gejala_terjawab_set = set(g.lower().strip() for g in gejala_terjawab if g.strip())
    
    for penyakit in basis_pengetahuan:
        aturan_penyakit_set = set(a.lower().strip() for a in penyakit["aturan"] if a.strip())
        
        cocok_gejala = gejala_terjawab_set.intersection(aturan_penyakit_set)
        
        if not aturan_penyakit_set:
            persen = 0
        else:
            persen = len(cocok_gejala) / len(aturan_penyakit_set)
            
        if persen > 0:
            cf = round(persen * penyakit["cf"], 2)
            hasil.append({
                "penyakit": penyakit["nama"],
                "cf": cf,
                "saran": penyakit["saran"],
                "gejala_tidak_ada": sorted(list(aturan_penyakit_set - gejala_terjawab_set))
            })
    
    hasil = sorted(hasil, key=lambda x: x["cf"], reverse=True)
    return hasil