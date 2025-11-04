# Quiz Application

Django-based quiz application with course, session, and question management.

## Features

- Course and Session management
- Multiple choice questions
- Real-time feedback
- Progress tracking
- Statistics and results

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/Sey1tayd/Exam_.git
cd Exam_
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
SUPERUSER_USERNAME=admin
SUPERUSER_PASSWORD=admin123
SUPERUSER_EMAIL=admin@example.com
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuserauto
```

7. Collect static files:
```bash
python manage.py collectstatic
```

8. Run the development server:
```bash
python manage.py runserver
```

## Railway Deployment

### Prerequisites
- Railway account
- GitHub repository connected

### Environment Variables

Set the following environment variables in Railway:

- `SECRET_KEY`: Django secret key (generate a new one for production)
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Your Railway domain (e.g., `your-app.railway.app`)
- `DATABASE_URL`: Railway will provide this automatically if you add a PostgreSQL service
- `SUPERUSER_USERNAME`: Admin username
- `SUPERUSER_PASSWORD`: Admin password
- `SUPERUSER_EMAIL`: Admin email

### Steps

1. Connect your GitHub repository to Railway
2. Add a PostgreSQL service (optional, SQLite will be used by default)
3. Set environment variables in Railway dashboard
4. Deploy!

The application will automatically:
- Run migrations
- Create superuser from environment variables
- Collect static files
- Start the Gunicorn server

### Access Admin Panel

Visit: `https://your-app.railway.app/admin/`

Login with credentials from `SUPERUSER_USERNAME` and `SUPERUSER_PASSWORD`.

## Project Structure

```
quizsite/
├── manage.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── railway.json
├── .gitignore
└── quizsite/
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
└── quiz/
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── management/
    │   └── commands/
    │       └── createsuperuserauto.py
    └── templates/
        └── quiz/
            ├── course_list.html
            ├── session_detail.html
            ├── question_run.html
            └── result_summary.html
```

## License

MIT
