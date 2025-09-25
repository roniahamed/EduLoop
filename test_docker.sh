#!/bin/bash

echo "Testing Docker setup for Eduloop..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file from .env.example"
    echo "⚠️  Please edit .env file with your database credentials before running docker-compose up"
fi

# Check if required files exist
required_files=("Dockerfile" "docker-compose.yml" "requirements.txt" "manage.py")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file is missing"
        exit 1
    fi
done

echo ""
echo "🎉 Docker setup looks good!"
echo ""
echo "To start the application:"
echo "1. Edit .env file with your database credentials"
echo "2. Run: docker-compose up --build"
echo "3. Run migrations: docker-compose exec web python manage.py migrate"
echo "4. Create superuser: docker-compose exec web python manage.py createsuperuser"
echo "5. Access the app at: http://localhost:8010"
echo "6. Access admin at: http://localhost:8010/admin/"
