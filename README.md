# 🧩 Django Authentication & Invitation API

A robust **Django REST Framework**–based backend that provides **JWT authentication**, **user invitations**, and **password reset workflows** — all documented and testable through **Swagger UI** and **ReDoc**.

---

## 🚀 Features

- ✅ JWT Authentication using [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- ✅ User Invitation System (send, list, and accept invites)
- ✅ Password Reset Request & Approval flow
- ✅ Auto-generated API documentation with [drf-spectacular](https://drf-spectacular.readthedocs.io/)
- ✅ Swagger UI & ReDoc for easy API exploration
- ✅ Modular structure for integration with any frontend (React, Nuxt, Vue, Angular)

---

## 🛠️ Tech Stack

- **Python** 3.10+
- **Django** 5.x
- **Django REST Framework (DRF)**
- **Simple JWT** for token authentication
- **drf-spectacular** for OpenAPI schema and docs

---

## 📦 Installation Guide

Follow these steps to set up and run the project locally.

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/EricWanjohiMuturi/Invite-only-backend-system
cd your-backend-repo
```

2️⃣ Create and Activate a Virtual Environment

For Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

For Windows (PowerShell):
```bash
python -m venv venv
venv\Scripts\activate
```

3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

4️⃣ Configure Environment Variables
```bash
Create a .env file in your project root and add(use the .env_example_template that I have provided):
```

# Django Secret Key
```bash
SECRET_KEY=your-very-secret-key

# Debug mode (set to False in production)
DEBUG=True

# Allowed Hosts
ALLOWED_HOSTS=127.0.0.1,localhost

# Database (SQLite example)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# For PostgreSQL example:
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=your_db_name
# DB_USER=your_db_user
# DB_PASSWORD=your_db_password
# DB_HOST=localhost
# DB_PORT=5432
```

Make sure your settings.py uses python-decouple or os.environ to load these variables.

5️⃣ Apply Migrations
```bash
python manage.py migrate
```
6️⃣ Create a Superuser
```bash
python manage.py createsuperuser
```

7️⃣ Run the Development Server
```bash
python manage.py runserver
```

🌐 API Base URL
Once the server is running, the API is available at:
```bash
http://127.0.0.1:8000/api/
```

📚 API Documentation
🔹 Swagger UI (Interactive Docs)
```bash
👉 http://127.0.0.1:8000/api/docs/
```

🔹 ReDoc (Reference Docs)
```bash
👉 http://127.0.0.1:8000/api/redoc/
```
🔹 OpenAPI Schema (JSON)
```bash
👉 http://127.0.0.1:8000/api/schema/
```

🔐 Authentication (JWT)

This project uses JWT (JSON Web Tokens) for authentication.

Obtain Tokens
```bash
POST /api/auth/token/

{
  "email": "user@example.com",
  "password": "yourpassword"
}


Response:

{
  "access": "ACCESS_TOKEN",
  "refresh": "REFRESH_TOKEN"
}
```
Refresh Token
```bash
POST /api/auth/token/refresh/

{
  "refresh": "REFRESH_TOKEN"
}
```

📩 Endpoints Overview
```bash
| 👥 Authentication & User | Method | Description                                   |
|--------------------------|--------|-----------------------------------------------|
| /api/auth/token/        | POST   | Obtain JWT access & refresh tokens           |
| /api/auth/token/refresh/ | POST   | Refresh JWT access token                      |
| /api/auth/me/           | GET    | Get currently authenticated user info        |
```

✉️ Invitations
```bash
| ✉️ Invitations | Method | Description |
|---|---|---|
| /api/auth/invite/ | POST | Create and send a new user invitation |
| /api/auth/invitations/ | GET | List all invitations |
| /api/auth/accept-invite/ | POST | Accept an invitation using token or link |
```

🔑 Password Reset
```bash
| 🔑 Password Reset | Method | Description |
|---|---|---|
| /api/auth/password-reset-request/ | POST | Create a password reset request |
| /api/auth/password-reset-approve/<int:request_id>/ | POST | Approve password reset request (admin only) |
| /api/auth/reset-password/ | POST | Confirm and set a new password |
| /api/auth/password-reset-requests/ | GET | List all password reset requests (admin only) |
```

🧭 How to Use Swagger Docs to Test Endpoints

Visit http://127.0.0.1:8000/api/docs/

Click Authorize and enter your JWT token (for protected routes).

Expand any section and click Try it out.

Enter input values and click Execute.

See the live response right below your request.

🧰 Development Tips

To reset your database:
```bash
python manage.py flush
```

To regenerate schema after changing serializers/views:
```bash
python manage.py spectacular --file schema.yml
```

To list all available routes:
```bash
python manage.py show_urls
```

🧾 Example Workflow

1️⃣ Invite a User → /api/auth/invite/
2️⃣ Accept Invite → /api/auth/accept-invite/
3️⃣ Login and Get JWT Token → /api/auth/token/
4️⃣ Access Protected Routes → /api/auth/me/
5️⃣ Request Password Reset → /api/auth/password-reset-request/

🧩 Postman Collection Setup

You can test the endpoints directly in Postman:

Open Postman and create a new workspace.

Click Import → Link.

Paste your OpenAPI URL:

http://127.0.0.1:8000/api/schema/


Postman will automatically generate all endpoints from the schema.

You can now test all APIs directly, including authentication flows.

💡 Tip: Save your JWT access token as a global variable in Postman and set it in Authorization: Bearer {{token}}.

🧑‍💻 Project Structure (Simplified)
```bash
project_root/
│
├── userauth/
│   ├── views.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── ...
│
├── project_name/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── manage.py
├── requirements.txt
└── .env
```
🧱 Example Admin Panel Access

Visit: http://127.0.0.1:8000/admin/

Login using your superuser credentials.

🧠 Notes

All endpoints are RESTful and JSON-based.

Token authentication required for protected routes:
Authorization: Bearer <access_token>

Use drf-spectacular to generate and update your OpenAPI schema anytime.