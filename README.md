# AGCBO Digital Hub

A comprehensive web platform for Aminia Gikambura Community Based Organisation (CBO) - a Youth Community Based Organisation in Kenya.

**Django-only deployment:** The site can be run entirely on Django (no Node.js). All public pages (home, about, projects, events, gallery, sports, reports, contact, login, register, dashboard) are served by the **pages** app using Django templates. This allows hosting the full site on **PythonAnywhere** or any Python/Django host. See [DEPLOYMENT.md](DEPLOYMENT.md).

## Project Structure

```
CBO/
├── backend/              # Django backend (full site + API)
│   ├── agcbo/           # Main Django project
│   ├── core/            # Core app with User model
│   ├── pages/            # Web pages (templates, views) – Django-only frontend
│   ├── members/         # Member management
│   ├── projects/        # Project management
│   ├── funding/         # Funding & donations
│   ├── events/          # Events & activities
│   ├── gallery/         # Media gallery
│   ├── sports/          # Sports programs
│   ├── gamification/    # Points, badges, leaderboard
│   └── reports/         # Reporting system
├── frontend/            # (Optional) Next.js frontend – not required for PythonAnywhere
│   ├── src/
│   │   ├── components/  # Reusable components
│   │   ├── pages/       # Page components
│   │   ├── hooks/       # Custom hooks
│   │   ├── services/    # API services
│   │   └── utils/       # Utilities
│   └── public/
└── requirements.txt     # Python dependencies
```

## Tech Stack

### Backend
- Django 4.2+
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Celery + Redis
- Cloudinary

### Frontend
- React 18+
- Next.js 14+
- Tailwind CSS
- Framer Motion
- Axios

### Payments
- M-Pesa (Daraja API)
- PayPal / Stripe

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Redis

### Backend Setup

1. Create virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Load seed data:
```bash
python manage.py seed_data
```

7. Run development server:
```bash
python manage.py runserver
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env.local
# Edit .env.local with your API URL
```

3. Run development server:
```bash
npm run dev
```

## Deployment to PythonAnywhere

### Backend Deployment

1. Upload backend folder to PythonAnywhere
2. Set up virtual environment
3. Install dependencies
4. Configure PostgreSQL database
5. Set environment variables
6. Run migrations
7. Collect static files: `python manage.py collectstatic`
8. Configure WSGI file

### Frontend Deployment

1. Build production version: `npm run build`
2. Upload build folder or deploy to Vercel/Netlify
3. Configure API endpoints

## Features

- Public website with project showcase
- Member registration and dashboard
- Admin panel for management
- Gamification system (points, badges)
- Donation system (M-Pesa, PayPal)
- Event management
- Sports program tracking
- Gallery and media management
- Reporting system

## Design System

- **Primary**: Deep Green (#0d4f3c)
- **Secondary**: Red (#dc2626)
- **Accent**: Gold/Yellow (#fbbf24)
- **Fun Accents**: Teal (#14b8a6) & Sky Blue (#0ea5e9)

## License

Proprietary - AGCBO Digital Hub
