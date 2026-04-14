# EduLoop — Intelligent Quiz & Question Bank Platform

EduLoop is a powerful, easy-to-use backend API that helps educational institutions, coaching centers, and content creators build and deliver smart, structured, and personalized quizzes at scale.

It organizes your entire question bank with a clean hierarchical system — Groups → Subjects → Categories → Subcategories — making content management intuitive and scalable. Students enjoy a smooth, session-based quiz experience with smart question rotation, seen-question tracking, and flexible support for all major question types (MCQ, True/False, Fill-in-the-Blank, Math, Writing, and more).

Whether you're running daily practice tests, mock exams, or adaptive learning sessions, EduLoop simplifies question bank management, enables bulk uploads with error reporting, and provides secure, token-based access for students — all while giving admins full control and insightful dashboard statistics.

Built for performance and reliability, EduLoop helps you focus on creating great educational content while delivering a seamless and engaging quiz experience to your learners.

## Live Demo

[Live API](https://extrahanden.ai)


## Features

- Hierarchical content taxonomy: Groups, Subjects, Categories, SubCategories, and Questions
- Session-based quiz engine with stateful question delivery, seen-question tracking, and batch rotation
- `JSONField`-based flexible question metadata supporting multiple question types (MCQ, fill-in-the-blank, true/false, math, writing, etc.)
- Bulk question upload via a single API call with detailed per-row error reporting
- Custom access token authentication (`AccessKey` header scheme) for student-facing endpoints
- DRF `TokenAuthentication` and `SessionAuthentication` support for admin and staff users
- Admin dashboard API exposing aggregate statistics (groups, subjects, categories, questions, tokens, users)
- Full CRUD management for questions via admin-only endpoints with partial update support
- Redis-backed response caching for frequently queried data (e.g., group listings cached for 15 minutes)
- Rate limiting: 200 requests/minute (anonymous), 500 requests/minute (authenticated)
- GZip response compression middleware for optimized payload sizes
- CORS policy with trusted-origin allowlist and credential support
- Unfold-powered Django admin interface with a clean, modern UI
- Dockerized deployment with multi-stage builds, Gunicorn, and Nginx reverse proxy
- Comprehensive database indexing strategy, including composite and partial indexes, for high-throughput query performance

## Tech Stack

[![Django](https://img.shields.io/badge/Django-5.2.5-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.16.1-000000?style=flat&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-6.4.0-DC382D?style=flat&logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-23.0.0-499848?style=flat&logo=gunicorn&logoColor=white)](https://gunicorn.org/)
[![Nginx](https://img.shields.io/badge/Nginx-1.23-009639?style=flat&logo=nginx&logoColor=white)](https://nginx.org/)

| Layer | Technology |
|---|---|
| Framework | Django 5.2.5 + Django REST Framework 3.16.1 |
| Database | PostgreSQL 15 (via `psycopg2-binary`) |
| Cache | Redis 6.x (via `django-redis`) |
| Authentication | Custom `AccessKey` token auth + DRF `TokenAuthentication` + `SessionAuthentication` |
| Admin Interface | `django-unfold` |
| Filtering | `django-filter` with `SearchFilter` and `OrderingFilter` |
| Static Files | WhiteNoise |
| Web Server | Gunicorn (3 workers) behind Nginx |
| Containerization | Docker (multi-stage build) + Docker Compose |
| Configuration | `python-decouple` (`.env` based) |

## Prerequisites

| Software | Minimum Version |
|---|---|
| Python | 3.11 |
| PostgreSQL | 15 |
| Redis | 6.x |
| Docker | 24.x (optional, for containerized setup) |
| Docker Compose | 2.x (optional) |
| pip | 23+ |

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/roniahamed/eduloop.git
cd eduloop
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env` with your credentials (see [Environment Variables](#environment-variables) section).

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

### 7. Collect Static Files

```bash
python manage.py collectstatic --no-input
```

## Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key. Use a long, random string in production. |
| `DEBUG` | Set to `False` in production. |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames (e.g., `localhost,127.0.0.1,yourdomain.com`). |
| `POSTGRES_DB` | PostgreSQL database name. |
| `POSTGRES_USER` | PostgreSQL username. |
| `POSTGRES_PASSWORD` | PostgreSQL password. |
| `DB_PORT` | PostgreSQL port (default: `5432`). |

> Note: The `.env.example` file in the repository root provides a complete template.

## Running the Project

### Local Development

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

### With Gunicorn (Production-like)

```bash
gunicorn --config gunicorn.conf.py eduloop.wsgi:application
```

### With Docker Compose

```bash
# Build and start all services (app, PostgreSQL, Nginx)
docker compose up --build

# Run in detached mode
docker compose up -d --build

# Apply migrations inside the running container
docker compose exec app python manage.py migrate

# Create superuser inside the running container
docker compose exec app python manage.py createsuperuser
```

The application will be accessible through Nginx on port `8091` (mapped to container port `80`).

## API Endpoints

### Authentication

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/api/api-token-auth/` | Obtain a DRF auth token (username + password) | Public |
| `POST` | `/api/token-verify/` | Validate a student AccessKey token | Public |
| `POST` | `/api/token-generate/` | Generate a new student AccessKey token | Admin |
| `GET` | `/api/token-list/` | List all AccessKey tokens | Admin |
| `PUT` | `/api/token-update/` | Update an AccessKey token | Admin |
| `DELETE` | `/api/token-delete/` | Delete an AccessKey token | Admin |

### Users

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/current-user/` | Retrieve the authenticated user's profile | Authenticated |
| `PATCH` | `/api/current-user/` | Update the authenticated user's profile | Authenticated |
| `DELETE` | `/api/current-user/` | Delete the authenticated user's account | Authenticated |
| `GET/POST` | `/api/users/` | List all users / Create a user | Admin |
| `GET/PUT/PATCH/DELETE` | `/api/users/{id}/` | Retrieve, update, or delete a user | Admin |

### Content Taxonomy

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET/POST` | `/api/groups/` | List or create Groups | Admin (write), Public (read) |
| `GET/POST` | `/api/subjects/` | List or create Subjects | Admin (write), Public (read) |
| `GET` | `/api/subject/{group_id}/` | List Subjects within a specific Group | Public |
| `GET/POST` | `/api/categories/` | List or create Categories (with SubCategories) | Admin (write), Public (read) |
| `GET` | `/api/categories/list/` | List Categories (flat, without SubCategories) | Public |
| `GET` | `/api/categories/{subject_id}/` | List Categories for a specific Subject | Public |
| `GET/POST` | `/api/subcategories/` | List or create SubCategories | Admin (write), Public (read) |
| `GET` | `/api/subcategories/{category_id}/` | List SubCategories for a specific Category | Public |

### Questions

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/api/questions/` | Start a new quiz session and receive the first question | Public |
| `GET` | `/api/questions/` | Retrieve the next question in the active session | Public |
| `DELETE` | `/api/questions/` | Reset and clear the active quiz session | Public |
| `POST` | `/api/upload-questions/` | Bulk upload questions from a JSON array | Admin |
| `POST` | `/api/question/create/` | Create a single question | Admin |

### Admin Dashboard

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/dashboard/` | Overview statistics (totals for all entities) | Admin |
| `GET` | `/api/dashboard/recent-questions/` | Paginated, searchable, filterable question list | Admin |
| `GET/PUT/PATCH/DELETE` | `/api/dashboard/question/{question_id}/` | Retrieve, update, or delete a specific question | Admin |

## Project Structure

```
eduloop/
├── eduloop/                  # Django project configuration
│   ├── settings.py           # Main settings (DB, auth, cache, CORS, DRF config)
│   ├── urls.py               # Root URL configuration
│   ├── wsgi.py               # WSGI entry point
│   └── asgi.py               # ASGI entry point
│
├── questions/                # Core quiz and content taxonomy app
│   ├── models.py             # Group, Subject, Category, SubCategory, Question
│   ├── serializers.py        # Read/write serializers for all content models
│   ├── views.py              # ViewSets, quiz engine, dashboard, bulk upload
│   ├── urls.py               # Questions URL routing
│   ├── permissions.py        # IsAdminOrReadOnly custom permission
│   ├── middleware.py         # CustomSessionMiddleware
│   └── admin.py              # Admin registrations
│
├── users/                    # Authentication and user management app
│   ├── models.py             # AccessToken model (student auth)
│   ├── authentication.py     # Custom AccessKey TokenAuthentication backend
│   ├── serializers.py        # UserSerializer, AccessTokenSerializer
│   ├── views.py              # Token management, UserViewSet, CurrentUserView
│   └── urls.py               # Users URL routing
│
├── academy/                  # Academy app (reserved for future use)
├── teacher/                  # Teacher app (reserved for future use)
├── ai/                       # AI app (reserved for future use)
│
├── nginx/
│   └── nginx.conf            # Nginx reverse proxy configuration
│
├── staticfiles/              # Collected static files (auto-generated)
├── Dockerfile                # Multi-stage Docker build
├── docker-compose.yml        # Docker Compose (app + PostgreSQL + Nginx)
├── gunicorn.conf.py          # Gunicorn configuration
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management entry point
└── .env.example              # Environment variable template
```

## Running Tests and Migrations

### Run Tests

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test questions
python manage.py test users

# Run with verbosity
python manage.py test --verbosity=2
```

### Database Migrations

```bash
# Create new migrations after model changes
python manage.py makemigrations

# Apply all pending migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

## Deployment

### Docker (Recommended)

The project ships with a production-ready Docker Compose setup including PostgreSQL, the Django/Gunicorn application, and an Nginx reverse proxy.

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with production values (DEBUG=False, strong SECRET_KEY, real DB credentials)

# 2. Build and start services
docker compose up -d --build

# 3. Run migrations
docker compose exec app python manage.py migrate

# 4. Create superuser
docker compose exec app python manage.py createsuperuser
```

### Production Checklist

- Set `DEBUG=False` in `.env`.
- Set a strong, unique `SECRET_KEY`.
- Restrict `ALLOWED_HOSTS` to your production domain(s).
- Ensure `CSRF_TRUSTED_ORIGINS` and `CORS_ALLOWED_ORIGINS` include your frontend domain.
- Configure Redis with a stable hostname/password for production cache.
- Use HTTPS with valid TLS certificates (handled by Nginx or a load balancer).
- Enable `SECURE_PROXY_SSL_HEADER` if terminating SSL at a proxy layer.



## License

Copyright (c) 2025 Roni Ahamed (JVAI). All rights reserved.

This project is licensed under a **Custom Proprietary License**. The following terms apply:

- You are permitted to view and reference the source code for educational and evaluation purposes only.
- Commercial use, redistribution, modification, or deployment of this software, in whole or in part, is strictly prohibited without prior written permission from the copyright holder.
- Unauthorized copying, sublicensing, or resale of this software or its derivatives is not allowed.

See the [LICENSE](./LICENSE) file in the repository root for the full license text.

For licensing inquiries or permissions, contact [mdroniahamed56@gmail.com](mailto:mdroniahamed56@gmail.com).

## Contact

- **GitHub**: [@roniahamed](https://github.com/roniahamed)
- **Portfolio**: [roniahamed.com](https://www.roniahamed.com)
- **LinkedIn**: [Roni Ahamed](https://www.linkedin.com/in/roniahamed/)
- **Email**: [mdroniahamed56@gmail.com](mailto:mdroniahamed56@gmail.com)

If you find this project useful, please consider starring the repository on GitHub.
