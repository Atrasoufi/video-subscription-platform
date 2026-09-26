# 🎬 Video Subscription Platform

A simplified Netflix-like backend built with **Django** and **Django REST Framework**.
Users can subscribe to plans, watch premium videos, and track their watch history.

## 🚀 Features

- 🔐 JWT Authentication
- 👤 Custom User (email-based login)
- 📺 Video management (premium/free)
- 💳 Subscription plans with mock payment gateway
- 🔒 Content access control based on active subscription
- 📊 Watch history with progress tracking
- ⚡ Live updates via WebSocket
- 📖 Swagger/OpenAPI documentation

## 🛠️ Tech Stack

- Python 3.14
- Django 5.x
- Django REST Framework
- SimpleJWT
- Django Channels
- drf-spectacular (Swagger)

## 📦 Setup

```bash
git clone https://github.com/Atrasoufi/video-subscription-platform.git
cd video-subscription-platform

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 🔌 API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/token/` | Get JWT token |
| POST | `/api/token/refresh/` | Refresh token |
| POST | `/api/accounts/register/` | Register user |
| GET  | `/api/accounts/me/` | Current user |

### Subscriptions
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/subscriptions/plans/` | List plans |
| GET/POST | `/api/subscriptions/subscriptions/` | User subscriptions |
| GET | `/api/subscriptions/subscriptions/current/` | Active subscription |
| POST | `/api/subscriptions/subscriptions/{id}/cancel/` | Cancel |
| GET/POST | `/api/subscriptions/payments/` | Payments |
| POST | `/api/subscriptions/payments/{id}/verify/` | Mock verify |

### Videos
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/videos/` | List videos |
| POST | `/api/videos/` | Create (admin) |
| GET | `/api/videos/{id}/` | Retrieve (requires subscription) |
| POST | `/api/videos/{id}/watch/` | Save progress |
| GET | `/api/videos/history/` | Watch history |

## 🔄 Example Flow

1. Register → `POST /api/accounts/register/`
2. Login → `POST /api/token/`
3. Choose plan → `GET /api/subscriptions/plans/`
4. Create payment → `POST /api/subscriptions/payments/`
5. Verify payment → `POST /api/subscriptions/payments/{id}/verify/`
6. Watch video → `GET /api/videos/{id}/`
7. Save progress → `POST /api/videos/{id}/watch/`

## 📡 WebSocket

```
ws://127.0.0.1:8000/ws/videos/
```

Live updates for watch progress and video status.

## 📖 API Docs

- Swagger UI: `/api/docs/`
- OpenAPI Schema: `/api/schema/`

## 📄 License

MIT
