# Railway Deployment Guide

## Hızlı Başlangıç

### 1. GitHub'a Push Et

```bash
git init
git add .
git commit -m "Initial commit - Railway ready"
git branch -M main
git remote add origin https://github.com/Sey1tayd/Exam_.git
git push -u origin main
```

### 2. Railway'de Proje Oluştur

1. [Railway.app](https://railway.app) hesabına gir
2. "New Project" → "Deploy from GitHub repo"
3. Repository'yi seç: `Sey1tayd/Exam_`
4. Deploy başlar otomatik olarak

### 3. Environment Variables Ayarla

Railway Dashboard → Project → Variables sekmesinde şunları ekle:

```
SECRET_KEY=<50+ karakterlik güvenli key>
DEBUG=False
ALLOWED_HOSTS=*.railway.app,your-app-name.railway.app
SUPERUSER_USERNAME=admin
SUPERUSER_PASSWORD=<güçlü-şifre>
SUPERUSER_EMAIL=admin@example.com
```

**SECRET_KEY oluşturma:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 4. PostgreSQL Ekle (Önerilen)

1. Railway Dashboard → "+ New" → "Database" → "Add PostgreSQL"
2. PostgreSQL service eklendiğinde `DATABASE_URL` otomatik eklenir
3. Alternatif: SQLite kullanılabilir (production için önerilmez)

### 5. Deploy

Railway otomatik olarak:
- ✅ Dependencies yükler
- ✅ Migrations çalıştırır
- ✅ Superuser oluşturur
- ✅ Static files toplar
- ✅ Gunicorn ile başlatır

### 6. Domain Ayarla

Railway Dashboard → Settings → "Generate Domain" ile public domain al.

## Önemli Notlar

- **PORT**: Railway otomatik olarak `$PORT` environment variable'ı sağlar
- **Static Files**: WhiteNoise ile serve edilir
- **Database**: PostgreSQL eklenmezse SQLite kullanılır (ephemeral storage)
- **Logs**: Railway Dashboard → Deployments → Logs'tan görebilirsin

## Troubleshooting

### Build başarısız olursa:
- `requirements.txt` kontrol et
- Logs'u incele
- Python versiyonu uyumlu mu kontrol et (`runtime.txt`)

### Superuser oluşmuyorsa:
- Environment variables doğru mu kontrol et
- Logs'ta hata mesajı var mı bak
- Manuel: Railway → Service → Deploy Logs

### Static files görünmüyorsa:
- `collectstatic` çalıştı mı kontrol et
- WhiteNoise middleware aktif mi bak
- `STATIC_ROOT` ayarlı mı kontrol et

## Local Test

Production ayarlarıyla local test:

```bash
# .env dosyası oluştur
SECRET_KEY=test-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
SUPERUSER_USERNAME=admin
SUPERUSER_PASSWORD=admin123
SUPERUSER_EMAIL=admin@example.com

# Test et
python manage.py check --deploy
python manage.py migrate
python manage.py createsuperuserauto
python manage.py collectstatic --noinput
gunicorn quizsite.wsgi --bind 0.0.0.0:8000
```

## Admin Panel Erişimi

Deploy sonrası: `https://your-app.railway.app/admin/`

Kullanıcı adı: `SUPERUSER_USERNAME` değeri
Şifre: `SUPERUSER_PASSWORD` değeri
