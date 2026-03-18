# Autism Learning Platform - Django Setup

This document describes the Django implementation of the Autism Learning and Skill Development Platform with GCP support.

## Project Structure

```
Autism/
├── autism_platform/       # Django project config
│   ├── settings.py       # Supports SQLite (dev) and Cloud SQL (prod)
│   └── urls.py
├── accounts/             # Users, roles, authentication
├── children/             # Child profiles, assignments
├── learning/             # Modules, activities, admin
├── recommendations/      # Rule-based recommendation engine
├── core/                 # GCP storage utilities
├── templates/            # HTML templates
├── manage.py
└── requirements-django.txt
```

## Actors & Roles

| Actor | Role | Capabilities |
|-------|------|--------------|
| **Administrator** | `admin` | Manage modules, content, view system reports |
| **Parent/Guardian** | `parent` | Create child profiles, assign activities, view progress |
| **Child (Learner)** | Uses parent session | Access child-friendly dashboard, complete activities |
| **System** | Recommendation Engine | Suggests activities based on progress, difficulty, repetition |

## Quick Start

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements-django.txt

# Run migrations
python manage.py migrate

# Create superuser (Administrator)
python manage.py createsuperuser

# Seed sample modules and activities
python manage.py seed_sample_data

# Run development server
python manage.py runserver
```

Then visit:
- http://127.0.0.1:8000/ - Home
- http://127.0.0.1:8000/accounts/register/ - Register as parent
- http://127.0.0.1:8000/admin/ - Django admin (for Administrator)

## GCP Deployment

### Cloud SQL (PostgreSQL)

1. Create a Cloud SQL instance in GCP Console.
2. Set environment variables:
   - `GCP_DB_NAME`, `GCP_DB_USER`, `GCP_DB_PASSWORD`
   - `GCP_DB_HOST` (instance connection name or IP)
   - `GCP_DB_PORT` (default 5432)
3. Uncomment the Cloud SQL database config in `autism_platform/settings.py`.
4. Install: `pip install psycopg2-binary`

### Cloud Storage (Media Files)

1. Create a GCS bucket.
2. Install: `pip install django-storages google-cloud-storage`
3. Set `GOOGLE_APPLICATION_CREDENTIALS` to service account JSON path.
4. Uncomment the `DEFAULT_FILE_STORAGE` and `GS_BUCKET_NAME` lines in settings.

## Migration from Flask

The original Flask app (`app.py`) can remain for reference. The Django app uses different URLs:

| Flask | Django |
|-------|--------|
| `/parent` | `/children/parent/` |
| `/child` | `/children/child/<pk>/` (requires child ID) |
| `/admin` | `/learning/admin/` |
| `/color-match` | `/learning/activity/<pk>/?child=<pk>` |

## Creating an Administrator

Use `createsuperuser` then set `role=admin` in Django admin: Users → select user → Role: Administrator.
