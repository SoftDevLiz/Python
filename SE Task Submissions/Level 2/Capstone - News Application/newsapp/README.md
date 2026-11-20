# NewsApp – Django Capstone Project

A full-featured Django news application with a RESTful API, role-based
access control, email notifications, and automated tests.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Setup & Installation](#setup--installation)
3. [How to Run](#how-to-run)
4. [Architecture Overview](#architecture-overview)
5. [Models Explained](#models-explained)
6. [Roles & Permissions](#roles--permissions)
7. [The REST API](#the-rest-api)
8. [Signals Explained](#signals-explained)
9. [Running Tests](#running-tests)
10. [Concept Glossary](#concept-glossary)

---

## Project Structure

```
newsapp/
├── manage.py                  # Django CLI entry point
├── requirements.txt           # Python dependencies
│
├── newsproject/               # Django project configuration
│   ├── settings.py            # All app settings (DB, email, JWT, DRF)
│   └── urls.py                # Root URL dispatcher
│
└── news/                      # The main Django app
    ├── models.py              # Database models (CustomUser, Article, etc.)
    ├── serializers.py         # DRF serializers (JSON ↔ Python)
    ├── permissions.py         # Custom DRF permission classes
    ├── api_views.py           # REST API views
    ├── views.py               # HTML template views (browser)
    ├── forms.py               # Django forms for HTML views
    ├── urls.py                # URL routing (web + API)
    ├── signals.py             # Post-save side effects (email, API POST)
    ├── apps.py                # AppConfig + group/permission setup
    ├── admin.py               # Django admin configuration
    ├── tests.py               # Automated unit tests
    └── templates/news/        # HTML templates
        ├── base.html
        ├── home.html
        ├── article_detail.html
        ├── article_form.html
        ├── article_confirm_delete.html
        ├── editor_dashboard.html
        ├── newsletter_list.html
        ├── newsletter_detail.html
        ├── newsletter_form.html
        ├── register.html
        ├── login.html
        └── profile.html
```

---

## Setup & Installation

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up MariaDB

Start the MariaDB service, then run:

```sql
CREATE DATABASE newsdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'newsuser'@'localhost' IDENTIFIED BY 'newspassword';
GRANT ALL PRIVILEGES ON newsdb.* TO 'newsuser'@'localhost';
FLUSH PRIVILEGES;
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (for the admin panel)

```bash
python manage.py createsuperuser
```

---

## How to Run

```bash
python manage.py runserver
```

| URL | What you see |
|-----|-------------|
| `http://127.0.0.1:8000/` | Home page – latest articles |
| `http://127.0.0.1:8000/admin/` | Django admin panel |
| `http://127.0.0.1:8000/register/` | Create an account |
| `http://127.0.0.1:8000/editor/` | Editor dashboard |
| `http://127.0.0.1:8000/api/articles/` | REST API – article list |

---

## Architecture Overview

The app has **two parallel layers**:

```
Browser user  →  views.py  →  templates/  →  HTML response
API client    →  api_views.py  →  serializers.py  →  JSON response
```

Both layers share the same **models.py** (the single source of truth for data)
and the same **permissions.py** (role checks).

---

## Models Explained

### Publisher
A media organisation. Can have many editors and journalists affiliated with it.

### CustomUser (extends AbstractUser)
Django comes with a built-in `User` model. We *extend* it with `AbstractUser`
to add our own fields. Key extra fields:

| Field | Purpose |
|-------|---------|
| `role` | `'reader'`, `'journalist'`, or `'editor'` |
| `subscribed_publishers` | M2M – readers follow publishers |
| `subscribed_journalists` | M2M – readers follow individual journalists |
| `publisher` | FK – which organisation does this editor/journalist work for |

**Why override `save()`?** We use it to enforce business rules automatically:
- When a user is saved as a journalist, their reader subscription fields are
  cleared (they don't make sense for a journalist).
- When a user is saved as a reader, their publisher FK is set to `None`.

### Article
A news article. Important fields:

| Field | Purpose |
|-------|---------|
| `author` | FK to the journalist who wrote it |
| `publisher` | FK to the publication (optional; `NULL` = independent) |
| `approved` | `False` = draft, `True` = published |
| `approved_by` | FK to the editor who approved it |
| `approved_at` | Timestamp of approval |

### Newsletter
A curated list of articles. The key relationship is the **ManyToMany** to
`Article` — one newsletter can include many articles, and one article can
appear in many newsletters.

---

## Roles & Permissions

| Role | Can do |
|------|--------|
| **Reader** | View approved articles and newsletters; manage subscriptions |
| **Journalist** | Everything a reader can do + create/edit/delete their own articles and newsletters |
| **Editor** | View, edit, delete any article or newsletter + **approve** articles |

Permissions are managed in two complementary ways:

1. **Django Groups** (`apps.py`) — standard Django model-level permissions
   assigned to `Reader`, `Journalist`, `Editor` groups.
2. **Custom DRF permission classes** (`permissions.py`) — fine-grained
   per-endpoint control (e.g., "only the article's author OR an editor can
   edit it").

---

## The REST API

### Authentication

The API uses **JWT (JSON Web Tokens)**. The flow is:

```
1. POST /api/token/   {"username": "...", "password": "..."}
   → Returns {"access": "eyJ...", "refresh": "eyJ..."}

2. Include the access token in every subsequent request:
   Header: Authorization: Bearer eyJ...

3. When the access token expires (1 hour), refresh it:
   POST /api/token/refresh/   {"refresh": "eyJ..."}
   → Returns a new {"access": "eyJ..."}
```

### All Endpoints

| Method | Endpoint | Who can use it |
|--------|----------|---------------|
| POST | `/api/register/` | Anyone |
| POST | `/api/token/` | Anyone |
| POST | `/api/token/refresh/` | Anyone |
| GET | `/api/articles/` | All authenticated |
| POST | `/api/articles/` | Journalists only |
| GET | `/api/articles/<id>/` | All authenticated |
| PUT | `/api/articles/<id>/` | Author or Editor |
| DELETE | `/api/articles/<id>/` | Author or Editor |
| GET | `/api/articles/subscribed/` | Readers (returns subscribed content) |
| POST | `/api/articles/<id>/approve/` | Editors only |
| GET | `/api/newsletters/` | All authenticated |
| POST | `/api/newsletters/` | Journalists + Editors |
| GET | `/api/newsletters/<id>/` | All authenticated |
| PUT | `/api/newsletters/<id>/` | Author or Editor |
| DELETE | `/api/newsletters/<id>/` | Author or Editor |
| POST | `/api/approved/` | Internal (open) |
| GET | `/api/publishers/` | All authenticated |
| GET | `/api/profile/` | Returns your own profile |

---

## Signals Explained

Django **signals** are a publish-subscribe system built into the framework.
They let one part of your code react to something that happened in another
part, without those two parts directly referencing each other.

### How we use signals

In `signals.py` there are two signal handlers connected with `@receiver`:

```
post_save → CustomUser  →  assign_user_group()
post_save → Article     →  article_approved()
```

**`assign_user_group`** fires every time a new `CustomUser` is created. It
automatically adds the user to the correct Django permission group.

**`article_approved`** fires every time an `Article` is saved. It only acts
when the private flag `_approval_just_set = True` is present (set by the
editor view just before calling `.save()`). When it fires, it:
1. Collects the email addresses of all relevant subscribers.
2. Calls `send_mail()` to notify them.
3. POSTs a JSON payload to `/api/approved/` using the `requests` library.

### Why mock signals in tests?

We don't want tests to actually send emails or make HTTP calls. We use
`unittest.mock.patch` to replace the real functions with fake ones during tests,
then assert those fakes were called the right number of times with the right
arguments.

---

## Running Tests

```bash
python manage.py test news
```

The test suite covers:
- ✅ JWT registration, login, token refresh
- ✅ Role-based article visibility (readers vs editors)
- ✅ Subscription filtering (`/api/articles/subscribed/`)
- ✅ Create / update / delete permissions per role
- ✅ Editor approval workflow
- ✅ Newsletter CRUD with ownership checks
- ✅ The `/api/approved/` log endpoint
- ✅ Signal side effects (mocked email and POST)
- ✅ Boundary cases (unauthenticated, wrong owner, already approved)

---

## Concept Glossary

| Term | Meaning |
|------|---------|
| **AbstractUser** | Django's base user class that you can extend |
| **ManyToManyField** | A relationship where both sides can have many of the other |
| **ForeignKey** | A relationship where one record points to exactly one other record |
| **Signal** | A notification that fires automatically when something happens in Django |
| **Serializer** | Converts Python objects to JSON (and validates JSON input back to Python) |
| **Permission class** | A DRF class that decides whether a request is allowed |
| **JWT** | JSON Web Token – a signed string that proves who you are |
| **Queryset** | A lazy database query in Django (`Article.objects.filter(...)`) |
| **post_save** | A signal that fires after any model's `.save()` is called |
| **`@receiver`** | A decorator that connects a function to a signal |
| **`patch()`** | A testing tool that temporarily replaces a function with a mock |
