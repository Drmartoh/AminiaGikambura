# AGCBO Digital Hub - Detailed Setup Guide

## Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **PostgreSQL 14+** - [Download PostgreSQL](https://www.postgresql.org/download/)
- **Redis** - [Download Redis](https://redis.io/download)
- **Git** - [Download Git](https://git-scm.com/downloads)

## Step-by-Step Setup

### 1. Clone/Download the Project

```bash
cd CBO
```

### 2. Backend Setup

#### 2.1 Create Virtual Environment

```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### 2.2 Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 2.3 Set Up PostgreSQL Database

1. Create a new PostgreSQL database:
```sql
CREATE DATABASE agcbo_db;
CREATE USER agcbo_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE agcbo_db TO agcbo_user;
```

2. Or use psql command line:
```bash
createdb agcbo_db
```

#### 2.4 Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` file with your settings:
- Database credentials
- Secret key (generate a new one: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- Cloudinary credentials (sign up at [cloudinary.com](https://cloudinary.com))
- Email settings
- Payment gateway credentials (M-Pesa, PayPal, Stripe)

#### 2.5 Run Migrations

```bash
python manage.py migrate
```

#### 2.6 Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

#### 2.7 Seed Initial Data

```bash
python manage.py seed_data
```

This creates:
- Sample counties (Kiambu, Nairobi, Nakuru)
- Ministries (Youth, Agriculture, Sports, Environment)
- Project categories
- Funding sources
- Sponsors
- Badges
- Sport programs
- Sample announcement

#### 2.8 Collect Static Files

```bash
python manage.py collectstatic --noinput
```

#### 2.9 Run Development Server

```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

#### 3.1 Install Dependencies

Open a new terminal:

```bash
cd frontend
npm install
```

#### 3.2 Configure Environment Variables

```bash
cp .env.example .env.local
```

Edit `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

#### 3.3 Run Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 4. Celery Setup (Optional - for background tasks)

#### 4.1 Start Redis

```bash
# On Windows (if installed):
redis-server

# On macOS (with Homebrew):
brew services start redis

# On Linux:
sudo systemctl start redis
```

#### 4.2 Start Celery Worker

In a new terminal:

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
celery -A agcbo worker -l info
```

#### 4.3 Start Celery Beat (for scheduled tasks)

In another terminal:

```bash
cd backend
source venv/bin/activate
celery -A agcbo beat -l info
```

## Testing the Setup

1. **Backend API**: Visit `http://localhost:8000/api/` - You should see API endpoints
2. **Admin Panel**: Visit `http://localhost:8000/admin/` - Login with superuser credentials
3. **Frontend**: Visit `http://localhost:3000` - You should see the homepage

## Common Issues & Solutions

### Issue: Database connection error
**Solution**: Check PostgreSQL is running and credentials in `.env` are correct

### Issue: Module not found errors
**Solution**: Ensure virtual environment is activated and all dependencies are installed

### Issue: CORS errors
**Solution**: Check `CORS_ALLOWED_ORIGINS` in `backend/agcbo/settings.py` includes your frontend URL

### Issue: Static files not loading
**Solution**: Run `python manage.py collectstatic` and check `STATIC_ROOT` in settings

### Issue: Cloudinary upload errors
**Solution**: Verify Cloudinary credentials in `.env` and ensure account is active

## Next Steps

1. **Customize Logo**: Replace logo in `frontend/public/` or update logo component
2. **Configure Payments**: Set up M-Pesa, PayPal, or Stripe credentials
3. **Set Up Email**: Configure SMTP settings for email notifications
4. **Add Content**: Use admin panel to add projects, events, and other content
5. **Customize Design**: Modify Tailwind config and components to match your brand

## Production Deployment

### PythonAnywhere Setup

1. Upload backend folder to PythonAnywhere
2. Create virtual environment in PythonAnywhere console
3. Install dependencies
4. Set up PostgreSQL database (PythonAnywhere provides this)
5. Configure environment variables in PythonAnywhere dashboard
6. Set up WSGI file to point to `agcbo.wsgi.application`
7. Configure static files mapping
8. Run migrations and seed data

### Frontend Deployment

1. Build production version:
```bash
npm run build
```

2. Deploy to Vercel/Netlify:
   - Connect your repository
   - Set environment variables
   - Deploy

3. Or upload `out` folder to any static hosting service

## Support

For issues or questions, please contact the development team.
