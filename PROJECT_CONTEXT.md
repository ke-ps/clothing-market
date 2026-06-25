# PROJECT_CONTEXT

## Project Overview

This project is a clothing marketplace inspired by Wallapop.

Users can:

* Register and login using Firebase Authentication
* Create, edit and delete clothing listings
* Upload multiple images per listing
* Mark products as favorites
* Chat with sellers and buyers in real time
* Manage their own profile

The goal of the project is educational and portfolio-oriented, focusing on full-stack development and clean architecture.

---

## Technology Stack

### Frontend

* Angular
* TypeScript
* SCSS
* Angular Router
* Angular Services

### Backend

* FastAPI
* Python
* SQLAlchemy 2.x
* WebSockets

### Database

* MySQL (Aiven)

### Authentication

* Firebase Authentication

### Images

* Cloudinary

---

## Backend Architecture

Directory structure:

backend/app/

* core/
* db/
* modules/

Never create new architectural layers unless explicitly requested.

---

## Module Structure

Each module must follow:

module/

* router.py
* service.py
* repository.py

Responsibilities:

### router.py

Responsible only for:

* API endpoints
* request validation
* calling services

### service.py

Responsible only for:

* business logic

### repository.py

Responsible only for:

* database access

No business logic inside repositories.

No database access inside routers.

---

## Database Rules

Use SQLAlchemy 2.x.

Avoid raw SQL unless explicitly requested.

All database models must be defined inside:

app/db/models.py

Pydantic schemas must be defined inside:

app/db/schemas.py

---

## Authentication Rules

Authentication is handled by Firebase Authentication.

Passwords must never be stored in MySQL.

Store Firebase UID inside the users table.

Backend must validate Firebase tokens before accessing protected resources.

---

## Product Rules

A product represents a clothing item.

Products support multiple images.

Images must be stored separately from products.

Recommended relationship:

Product -> ProductImages

---

## Chat Rules

Real-time communication must use FastAPI WebSockets.

Messages must be persisted in MySQL.

A chat belongs to a product.

---

## Coding Standards

* Use English for all code.
* Use descriptive names.
* Use type hints whenever possible.
* Keep functions small and focused.
* Avoid duplicated logic.
* Follow existing project patterns before creating new ones.

---

## AI Assistant Rules

Before generating code:

1. Analyze the existing structure.
2. Reuse existing patterns.
3. Explain which files will be modified.
4. Do not add extra features not requested.
5. Do not refactor existing code unless explicitly requested.
6. Do not create unused files.
7. Respect the architecture described in this document.

When uncertain, ask for clarification instead of making assumptions.
