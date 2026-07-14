# ECE311 — Databases

Coursework repository for ECE311 Databases. It contains a Dockerized Django/MySQL backend for a course-notes application, database schema design files, and API endpoints for departments, courses, categories, posts, users, and reactions.

## Contents

| Path | Description |
|---|---|
| `backend/django_server/` | Django project and API application. |
| `backend/django_server/api/` | URL routes, views, and database service helpers for the notes API. |
| `backend/Dockerfile` | Backend image definition with Python, Django dependencies, and OpenVPN. |
| `database/schema.sql` | MySQL schema for users, departments, courses, categories, posts, reactions, and roles. |
| `database/init.sql` | Small seed dataset for local development. |
| `database/assignment.erdt` | ERD/design artifact for the database assignment. |
| `docker-compose.yml` | Local development stack with Django, MySQL, and phpMyAdmin. |

## Requirements

- Docker and Docker Compose
- A `.env` file based on `.env.example`
- UTH VPN credentials if the backend needs to call UTH SIS endpoints from inside the container

## Setup

Copy the example environment file and fill in the missing values:

```bash
cp .env.example .env
```

Generate a Fernet key for encrypted client cookies/tokens:

```bash
python3 - <<'PY'
import base64, os
print(base64.urlsafe_b64encode(os.urandom(32)).decode())
PY
```

Optionally generate a Django development secret key:

```bash
python3 - <<'PY'
import secrets, string
chars = string.ascii_letters + string.digits + string.punctuation
print(''.join(secrets.choice(chars) for _ in range(50)))
PY
```

Start the local stack:

```bash
docker compose up --build notes_app mysql phpmyadmin
```

The services expose:

| Service | URL |
|---|---|
| Django API | `http://localhost:9000/` |
| phpMyAdmin | `http://localhost:8080/` |

For a fresh MySQL volume, Docker initializes the database from:

```text
database/schema.sql
database/init.sql
```

If a database volume already exists, remove it first or apply the SQL files manually.

## Useful API routes

```text
GET  /department
GET  /department/courses
GET  /courses/<courseId>
GET  /courses/<courseId>/categories
GET  /categories/<courseId>/<categoryTitle>/posts
POST /categories/<courseId>/<categoryTitle>/posts
GET  /users/<userId>
GET  /users/<userId>/posts
GET  /posts/<postId>
GET  /posts/<postId>/reactions
PUT  /posts/<postId>/reactions
```

Most endpoints expect encrypted `x-jsessionid` and `x-sis-csrf-token` headers and validate the session against UTH SIS before returning data.
