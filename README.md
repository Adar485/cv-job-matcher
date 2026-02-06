<div align="center">

# 🎯 CV Job Matcher

### Yapay Zeka Destekli CV ve İş İlanı Eşleştirme Sistemi

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61dafb.svg)](https://reactjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791.svg)](https://postgresql.org)
[![BERT](https://img.shields.io/badge/BERT-Turkish-orange.svg)](https://huggingface.co/dbmdz/bert-base-turkish-cased)

<p align="center">
  <img src="https://img.shields.io/badge/NLP-Doğal%20Dil%20İşleme-purple.svg" alt="NLP"/>
  <img src="https://img.shields.io/badge/ML-Makine%20Öğrenmesi-red.svg" alt="ML"/>
</p>

---

**CV'nizi yükleyin, yapay zeka yeteneklerinizi analiz etsin ve size en uygun iş ilanlarını bulsun!**

[Özellikler](#-özellikler) •
[Teknolojiler](#-teknolojiler) •
[Kurulum](#-kurulum) •
[Kullanım](#-kullanım) •
[API](#-api-endpoints)

</div>

---

## 📋 Proje Hakkında

CV Job Matcher, NLP (Doğal Dil İşleme) teknolojileri kullanarak CV'leri analiz eden ve iş ilanlarıyla akıllı eşleştirme yapan bir web uygulamasıdır. BERT modeli ile semantik analiz yaparak, sadece anahtar kelime eşleşmesi değil, anlam bazlı eşleştirme sağlar.

## ✨ Özellikler

| Özellik | Açıklama |
|---------|----------|
| 📄 **PDF CV Parsing** | PyMuPDF ile PDF'den otomatik metin çıkarma |
| 🧠 **BERT Analizi** | Türkçe BERT modeli ile semantik embedding oluşturma |
| 🔍 **Yetenek Çıkarma** | CV ve iş ilanlarından otomatik skill detection |
| 📊 **Akıllı Eşleştirme** | Cosine Similarity ile %0-100 eşleşme skoru |
| 🎯 **Detaylı Skorlama** | Semantic benzerlik + Yetenek eşleşmesi analizi |
| 🔐 **Güvenli Auth** | JWT tabanlı kimlik doğrulama |
| 💼 **İş İlanı Yönetimi** | İlan oluşturma, listeleme, yetenek analizi |

## 🛠 Teknolojiler

### Backend
```
FastAPI         → Modern, hızlı Python web framework
PostgreSQL      → Güçlü ilişkisel veritabanı
SQLAlchemy      → Python ORM
Transformers    → Hugging Face BERT modeli
PyMuPDF         → PDF işleme
scikit-learn    → Cosine similarity hesaplama
JWT             → Token tabanlı authentication
```

### Frontend
```
React 18        → Kullanıcı arayüzü
React Router    → Sayfa yönlendirme
Axios           → API istekleri
```

### NLP & ML
```
BERT Turkish    → dbmdz/bert-base-turkish-cased
Sentence Embed  → 768 boyutlu vektör temsili
Cosine Sim      → Metin benzerliği ölçümü
```

## 📁 Proje Yapısı
```
cv-job-matcher/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI uygulaması
│   │   ├── config.py            # Ayarlar
│   │   ├── database.py          # DB bağlantısı
│   │   ├── models/              # SQLAlchemy modelleri
│   │   │   ├── user.py
│   │   │   ├── cv.py
│   │   │   └── job.py
│   │   ├── schemas/             # Pydantic şemaları
│   │   ├── routers/             # API endpoint'leri
│   │   │   ├── auth.py
│   │   │   ├── cv.py
│   │   │   └── job.py
│   │   ├── services/            # İş mantığı
│   │   │   ├── cv_parser.py     # PDF parsing
│   │   │   ├── nlp_engine.py    # BERT işlemleri
│   │   │   └── matcher.py       # Eşleştirme algoritması
│   │   └── utils/
│   │       └── auth.py          # JWT işlemleri
│   ├── requirements.txt
│   └── uploads/                 # Yüklenen CV'ler
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Navbar.js
│   │   ├── pages/
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── Dashboard.js
│   │   │   ├── Upload.js
│   │   │   └── Jobs.js
│   │   ├── services/
│   │   │   └── api.js
│   │   └── App.js
│   └── package.json
└── README.md
```

## 🚀 Kurulum

### Gereksinimler

- Python 3.10+
- Node.js 18+
- PostgreSQL 15+
- Git

### 1. Projeyi Klonlayın
```bash
git clone https://github.com/Adar485/cv-job-matcher.git
cd cv-job-matcher
```

### 2. PostgreSQL Veritabanı
```sql
CREATE DATABASE cv_job_matcher;
```

### 3. Backend Kurulumu
```bash
cd backend

# Virtual environment oluştur
python -m venv venv

# Aktif et (Windows)
venv\Scripts\activate

# Paketleri yükle
pip install -r requirements.txt

# Sunucuyu başlat
uvicorn app.main:app --reload
```

Backend: http://127.0.0.1:8000

### 4. Frontend Kurulumu
```bash
cd frontend

# Paketleri yükle
npm install

# Uygulamayı başlat
npm start
```

Frontend: http://localhost:3000

## 📖 Kullanım

### 1. Kayıt & Giriş
- Yeni hesap oluşturun veya giriş yapın

### 2. CV Yükleme
- PDF formatında CV'nizi yükleyin
- Sistem otomatik olarak:
  - Metni çıkarır
  - Yetenekleri tespit eder
  - BERT embedding oluşturur

### 3. İş İlanı Ekleme
- Yeni iş ilanları ekleyin
- Sistem otomatik olarak aranan yetenekleri çıkarır

### 4. Eşleştirme
- "İşlerle Eşleştir" butonuna tıklayın
- Sonuçları görün:
  - **Final Skor**: Genel eşleşme yüzdesi
  - **Semantic Benzerlik**: BERT tabanlı anlam benzerliği
  - **Yetenek Eşleşmesi**: Ortak yetenekler

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Açıklama |
|--------|----------|----------|
| POST | `/api/auth/register` | Yeni kullanıcı kaydı |
| POST | `/api/auth/login` | Giriş ve token alma |
| GET | `/api/auth/me` | Kullanıcı bilgileri |

### CV İşlemleri
| Method | Endpoint | Açıklama |
|--------|----------|----------|
| POST | `/api/cv/upload` | CV yükleme |
| GET | `/api/cv/` | CV listesi |
| GET | `/api/cv/{id}/skills` | CV yetenekleri |
| DELETE | `/api/cv/{id}` | CV silme |

### İş İlanları
| Method | Endpoint | Açıklama |
|--------|----------|----------|
| POST | `/api/jobs/` | İlan oluşturma |
| GET | `/api/jobs/` | İlan listesi |
| GET | `/api/jobs/{id}/skills` | İlan yetenekleri |
| POST | `/api/jobs/{cv_id}/match` | CV-İş eşleştirme |

## 📊 Eşleştirme Algoritması
```
Final Skor = (0.6 × Semantic Benzerlik) + (0.4 × Yetenek Eşleşmesi)

Semantic Benzerlik: BERT embedding'leri arası cosine similarity
Yetenek Eşleşmesi: Ortak yetenek sayısı / Toplam aranan yetenek
```

## 🔍 Tespit Edilen Yetenekler

Sistem şu yetenekleri otomatik tespit eder:

**Programlama:** Python, Java, JavaScript, C++, C#, Go, Rust, TypeScript...

**Web:** React, Angular, Vue, Node.js, Django, FastAPI, Flask...

**Veritabanı:** SQL, PostgreSQL, MySQL, MongoDB, Redis...

**DevOps:** Docker, Kubernetes, AWS, Azure, Git, Linux...

**ML/AI:** Machine Learning, Deep Learning, TensorFlow, PyTorch...

## 👨‍💻 Geliştirici

**Adar Bilmez**

- GitHub: [@Adar485](https://github.com/Adar485)

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

---

<div align="center">

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!

</div>
