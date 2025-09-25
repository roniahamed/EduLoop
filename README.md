# Eduloop

## Description
Eduloop is a Django-based educational platform designed for managing and organizing questions for quizzes, assessments, or educational content. It provides a structured way to categorize questions by groups, subjects, categories, and subcategories. The platform includes AI integration capabilities and uses access tokens for authentication. Importantly, Eduloop does not track student data or maintain student accounts.

## Features
- Hierarchical question organization (Groups -> Subjects -> Categories -> Subcategories -> Questions)
- RESTful API for question management
- Session-based question retrieval for quiz functionality
- Bulk question upload
- Access token-based authentication
- Admin interface with Django Unfold
- AI integration ready (via pythagora-core module)

## Tech Stack
- **Backend**: Django 5.2.5, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: Token-based
- **Admin Interface**: Django Unfold
- **Deployment**: Gunicorn, Whitenoise
- **Other**: Python Decouple for configuration

## Installation

### Option 1: Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/roniahamed/EduLoop
   cd eduloop
   ```

2. Copy the environment file:
   ```bash
   cp .env.example .env
   ```

3. Edit the `.env` file with your settings:
   ```bash
   nano .env  # or use your preferred editor
   ```

4. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

5. Run migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

7. Access the application:
   - Web application: http://localhost:80
   - Admin interface: http://localhost:80/admin/

### Option 2: Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/roniahamed/EduLoop
   cd eduloop
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

4. Set up environment variables:
   Create a `.env` file with:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   DB_NAME=your-db-name
   DB_USER=your-db-user
   DB_PASSWORD=your-db-password
   DB_HOST=127.0.0.1
   DB_PORT=5432
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## User Interface

Eduloop provides a modern graphical user interface through the Django Unfold admin interface:
- Access the admin panel at `/admin/` for managing questions, groups, subjects, categories, and access tokens
- The admin interface features a clean, responsive design with intuitive navigation
- Supports bulk operations and advanced filtering for efficient content management

For API consumers, the platform offers RESTful endpoints for programmatic access.

## Usage

- Access the admin interface at `/admin/` to manage questions and access tokens.
- Use the API endpoints to interact with the platform programmatically.

## Docker Setup

### Services
- **web**: Django application running on Gunicorn (port 8010)
- **db**: PostgreSQL database (port 5432)

### Docker Commands

```bash
# Build and start all services
docker-compose up --build

# Start services in background
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Execute commands in the web container
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Rebuild and restart
docker-compose down
docker-compose up --build

# Clean up (removes containers, networks, and volumes)
docker-compose down -v
```

### Environment Variables
Copy `.env.example` to `.env` and configure:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False in production
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password

## API Documentation

For detailed API documentation, including request/response examples, authentication details, and endpoint specifications, see [docs/api.md](docs/api.md).

### Quick API Endpoints Overview

#### Authentication
- `POST /api/token-verify/`: Validate an access token
- `POST /api/api-token-auth/`: Obtain authentication token (if using DRF token auth)

#### Questions Management
- `GET/POST /api/groups/`: List or create groups
- `GET/POST /api/subjects/`: List or create subjects
- `GET /api/subject/{group_id}/`: List subjects for a specific group
- `GET/POST /api/categories/`: List or create categories
- `GET /api/categories/{subject_id}/`: List categories for a specific subject
- `GET/POST /api/subcategories/`: List or create subcategories
- `GET /api/subcategories/{category_id}/`: List subcategories for a specific category
- `GET/POST/DELETE /api/questions/`: Retrieve questions, start a question session, or reset session
- `POST /api/upload-questions/`: Bulk upload questions

## Models

### Questions App
- **Group**: Top-level organizational unit
- **Subject**: Belongs to a Group
- **Category**: Belongs to a Subject and Group
- **SubCategory**: Belongs to a Category, Subject, and Group
- **Question**: The core model with level, type, and metadata. Belongs to Group, Subject, Category, and optionally SubCategory.

### Users App
- **AccessToken**: For authentication, with description and active status.

## Data Privacy
This application does not collect, store, or track any personal data related to students. It does not maintain student accounts or profiles. All functionality is focused on question management and organization for educational purposes.

## Changelog

### [Version 1.0.0] - Initial Release
- Implemented hierarchical question organization system
- Added RESTful API endpoints for question management
- Integrated Django Unfold for modern admin interface
- Added access token authentication
- Bulk question upload functionality
- Session-based question retrieval for quizzes

## Author

Developed by Roni Ahamed

## License

This software is proprietary and not free for any use. All rights reserved.

For licensing inquiries, please contact the project maintainers.
