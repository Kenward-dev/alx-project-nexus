# 🗳️ Poll API

A simple RESTful API built with Django REST Framework that allows authenticated users to create, publish, and vote on polls.

**🔗 Live URL:** [https://sudden-erica-kenward-9447691a.koyeb.app](https://sudden-erica-kenward-9447691a.koyeb.app)  
**📦 GitHub Repo:** [Kenward-dev/alx-project-nexus](https://github.com/Kenward-dev/alx-project-nexus/)

---

## 🚀 Features

- User registration & authentication using **Djoser + JWT**
- Create polls with multiple choices (via comma-separated input)
- Publish polls immediately or leave as drafts
- Authenticated users can vote once per poll
- Poll results visible after poll ends
- Admin and creator-only access to certain actions

---

## 🔧 API Endpoints

### 📊 Polls

| Method | Endpoint                  | Description                        |
|--------|---------------------------|------------------------------------|
| POST   | `/polls/`                 | Create a new poll (with choices)   |
| POST   | `/polls/{id}/publish/`   | Publish a draft poll               |
| GET    | `/polls/`                 | List all polls                     |
| GET    | `/polls/{id}/`           | Get details of a single poll       |
| GET    | `/polls/{id}/results/`   | View poll results (after expiry)   |

### 🗳️ Voting

| Method | Endpoint      | Description                  |
|--------|---------------|------------------------------|
| POST   | `/vote/`      | Vote on a poll               |
| GET    | `/vote/`      | View your voting history     |

### 🔐 Authentication (via Djoser)

| Method | Endpoint                                  | Description                            |
|--------|-------------------------------------------|----------------------------------------|
| POST   | `/auth/users/`                            | Register a new user                    |
| POST   | `/auth/users/activation/`                 | Activate account (after email)         |
| POST   | `/auth/jwt/create/`                       | Obtain JWT access and refresh tokens   |
| POST   | `/auth/jwt/refresh/`                      | Refresh JWT access token               |
| POST   | `/auth/jwt/verify/`                       | Verify token validity                  |
| POST   | `/auth/users/reset_password/`             | Send password reset link               |
| POST   | `/auth/users/reset_password_confirm/`     | Confirm password reset                 |
| GET    | `/auth/users/me/`                         | Get current authenticated user         |

---

## 📦 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Kenward-dev/alx-project-nexus.git
   cd alx-project-nexus

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file**

   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   DATABASE_URL=sqlite:///db.sqlite3
   FRONTEND_URL=http://localhost:3000
   ```

4. **Run migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server**

   ```bash
   python manage.py runserver
   ```

---

## 🧪 Example: Poll Creation (POST `/polls/`)

```json
{
  "question": "What is your favorite animal?",
  "choices": "Cat, Dog, Rabbit",
  "is_draft": false
}
```

---

## ✅ Voting Constraints

* Users can vote only once per poll
* Votes allowed only while poll is active
* Changing vote is allowed before poll ends
* Users cannot vote on their own polls

---

## ⚙️ Tech Stack

* Django & Django REST Framework
* Djoser + SimpleJWT for Auth
* Python-Decouple + dj-database-url
* SQLite (Dev) / PostgreSQL (Prod)
* Koyeb for deployment
* GitHub Actions (CI-ready)

---

## 🧑‍💻 Author

**Kenward Terhemba**
📫 [GitHub Profile](https://github.com/Kenward-dev)

---

