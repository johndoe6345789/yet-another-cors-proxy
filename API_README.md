# Flask API Proxy App

A simple Flask application with authentication and API proxy capabilities.

## Features

- **Simple Authentication**: Username/password authentication with secure password hashing
- **API Proxy Endpoints**: Proxy requests to external URLs with configurable endpoints
- **Permissive CORS**: CORS enabled by default for easy API access
- **Dockerized**: Ready to deploy with Docker and Docker Compose
- **CI/CD Pipeline**: GitHub Actions workflow for automated building and testing

## Quick Start with Docker

### Using Docker Compose (Recommended)

```bash
docker-compose up --build
```

The application will be available at `http://localhost:5000`

### Using Docker directly

```bash
# Build the image
docker build -t flask-app-template .

# Run the container
docker run -p 5000:5000 flask-app-template
```

## Local Development

### Requirements

- Python 3.8.5+
- pipenv

### Installation

1. Clone the repository:
```bash
git clone http://github.com/johndoe6345789/flask-app-template
cd flask-app-template
```

2. Install dependencies:
```bash
pipenv install
```

3. Initialize the database:
```bash
pipenv run python init_db.py
```

4. Run the application:
```bash
pipenv run python run.py
```

The application will be available at `http://localhost:5000`

## Default Credentials

After running `init_db.py`, you can log in with:
- **Username**: `admin`
- **Password**: `admin123`

**IMPORTANT**: Change the default password after first login!

## API Endpoints

### Authentication

#### Login (Web Form)
- **URL**: `/login/`
- **Method**: `GET`, `POST`
- **Description**: Web form login

#### API Login
- **URL**: `/api/auth/login`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Body**:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

#### API Logout
- **URL**: `/api/auth/logout`
- **Method**: `POST`
- **Authentication**: Required

#### Check Auth Status
- **URL**: `/api/auth/status`
- **Method**: `GET`
- **Description**: Check if user is authenticated

### Proxy Endpoints

#### Proxy Requests
- **URL**: `/api/proxy/<proxy_name>`
- **Methods**: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`
- **Description**: Proxy requests to configured external URLs

To configure proxy endpoints, edit `app/configuration.py`:

```python
PROXY_ENDPOINTS = {
    '/api/proxy/example': 'https://api.example.com',
    '/api/proxy/jsonplaceholder': 'https://jsonplaceholder.typicode.com'
}
```

Example usage:
```bash
# Proxy to https://jsonplaceholder.typicode.com/posts/1
curl http://localhost:5000/api/proxy/jsonplaceholder/posts/1
```

## CORS Configuration

CORS is enabled by default with permissive settings. You can customize it in `app/configuration.py`:

```python
CORS_ORIGINS = "*"  # Allow all origins
CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = "*"
```

## Configuration

All configuration is in `app/configuration.py`. You can switch between configurations:

- `DevelopmentConfig` (default)
- `ProductionConfig`
- `TestingConfig`

Edit `app/__init__.py` to change the active configuration.

## GitHub Actions Workflow

The repository includes a CI/CD workflow (`.github/workflows/build-test.yml`) that:

1. Checks Python syntax
2. Builds the Docker image
3. Tests the Docker image by running it and checking the health endpoint

The workflow runs automatically on push and pull requests.

## License

GPLv3
