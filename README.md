# CSGO Panel

A Django-powered web panel for CS:GO community servers with player statistics, premium subscriptions, and server management.

## Features

- **Steam Authentication** - Login via Steam OpenID
- **Player Statistics** - View player stats from game servers (kills, deaths, K/D, playtime, etc.)
- **Premium Subscriptions** - Sell VIP/Premium access with Stripe and Khalti payment gateways
- **Server Status** - Live game server status queries using OpenGSQ
- **Discord Integration** - Send reports, appeals, and contact forms to Discord webhooks
- **Multi-Server Support** - Manage multiple game servers with separate stats databases
- **Admin Management** - Automatic SourceMod admin creation for premium users

## Requirements

- Python 3.9+
- MySQL 8.0+ (for main database)
- Docker (optional, for running MySQL locally)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd academy-csgo
```

### 2. Create Virtual Environment

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Database

**Option A: Using Docker (Recommended)**
```bash
docker run -d \
  --name academy-mysql \
  -e MYSQL_ROOT_PASSWORD=my-secret-pw \
  -e MYSQL_DATABASE=panel \
  -p 3306:3306 \
  mysql:8.0
```

**Option B: Using existing MySQL**
- Create a database named `panel`
- Note down your connection credentials

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Required
SECRET_KEY='your-secure-secret-key'
FERNET_KEY='your-32-byte-base64-encoded-key'
DB_DEFAULT_URL='mysql://root:my-secret-pw@127.0.0.1:3306/panel'

# Steam API (Required for authentication)
STEAM_API_KEY='your-steam-api-key'

# Django Settings
DEBUG_VALUE=1
DJANGO_ALLOWED_HOSTS='127.0.0.1,localhost'
SITE_URL='http://127.0.0.1:8000'

# Discord Webhooks (Optional)
REPORT_DISCORD_WEBHOOK_URL='https://discord.com/api/webhooks/...'
APPEAL_DISCORD_WEBHOOK_URL='https://discord.com/api/webhooks/...'
CONTACT_DISCORD_WEBHOOK_URL='https://discord.com/api/webhooks/...'

# Payment Gateways (Optional)
STRIPE_SK='sk_...'
STRIPE_WH_SECRET='whsec_...'
KHALTI_API_SECRET_KEY='...'

# Email (Optional)
EMAIL_HOST='smtp.sendgrid.net'
EMAIL_HOST_USER='apikey'
EMAIL_HOST_PASSWORD='your-sendgrid-api-key'
EMAIL_PORT='587'
SERVER_EMAIL='noreply@yourdomain.com'

# Error Tracking (Optional)
SENTRY_DSN='https://...@sentry.io/...'

# Admin Info
ADMIN_ONE_NAME='Admin Name'
ADMIN_ONE_EMAIL='admin@example.com'
```

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Django secret key for cryptographic signing |
| `FERNET_KEY` | Yes | Key for encrypting database credentials (32-byte base64) |
| `DB_DEFAULT_URL` | Yes | Main database connection URL |
| `STEAM_API_KEY` | Yes | Steam Web API key from https://steamcommunity.com/dev/apikey |
| `DEBUG_VALUE` | No | Set to `1` for development, `0` for production |
| `DJANGO_ALLOWED_HOSTS` | No | Comma-separated list of allowed hosts |
| `SITE_URL` | No | Full URL of your site (for payment callbacks) |
| `STRIPE_SK` | No | Stripe secret key for payments |
| `STRIPE_WH_SECRET` | No | Stripe webhook secret |
| `KHALTI_API_SECRET_KEY` | No | Khalti payment gateway API key |
| `SENTRY_DSN` | No | Sentry DSN for error tracking |
| `*_DISCORD_WEBHOOK_URL` | No | Discord webhook URLs for notifications |

## How It Works

### Architecture

```
academy-csgo/
├── csgo/              # Django project settings
├── stats/             # Player stats, servers, VIP management
├── steam/             # Steam authentication & user profiles
├── store/             # Premium store & payment processing
├── templates/         # HTML templates
└── static/            # CSS, JS, images
```

### Core Components

**1. Steam Authentication (`steam/`)**
- Uses `social-auth-app-django` for Steam OpenID login
- Creates user profiles with Steam avatar and nickname
- Stores SteamID64 for linking game stats

**2. Server Management (`stats/models.py`)**
- `Server` model stores game server info (IP, port, display name)
- Optional `stats_db_url` connects to external stats database (e.g., LevelsRanks)
- Servers without stats URL work as display-only

**3. Player Statistics (`stats/views.py`)**
- Queries external MySQL databases for player stats
- Uses `LvlBase` model mapped to `lvl_base` table (LevelsRanks plugin)
- Supports multiple game servers with separate databases

**4. Premium System (`store/`)**
- Products linked to servers with duration (days)
- Payment via Stripe or Khalti
- Auto-creates SourceMod admin entries in `sm_admins` table
- VIP entries auto-expire based on duration

**5. Discord Integration (`stats/discord.py`)**
- Report Player form sends to Discord webhook
- Appeal Ban form sends to Discord webhook
- Contact Us form sends to Discord webhook

### Database Schema

**Main Database (panel)**
- Django models: Users, Servers, Products, VIPs, Purchases

**Stats Databases (per server, optional)**
- `lvl_base` - Player statistics (LevelsRanks plugin)
- `sm_admins` - SourceMod admin entries

### Adding a New Server

1. Go to Django Admin (`/admin/`)
2. Add new Server with:
   - `display_name`: Shown in UI
   - `server_hostname`: IP:Port (e.g., `192.168.1.1:27015`)
   - `stats_db_url` (optional): `mysql://user:pass@host:port/dbname`
   - `selling_premium`: Enable to show in store

3. If stats database is configured:
   - Server appears in Stats navigation
   - Player profiles show stats from this server
   - Premium purchases create admin entries

## Production Deployment

### Using Gunicorn (Linux/Mac)

```bash
gunicorn csgo.wsgi:application --bind 0.0.0.0:8000
```

### Using Waitress (Windows)

```bash
waitress-serve --port=8000 csgo.wsgi:application
```

### Production Checklist

1. Set `DEBUG_VALUE=0` in `.env`
2. Set `DJANGO_ALLOWED_HOSTS` to your domain
3. Configure `SITE_URL` with your production URL
4. Set up HTTPS (required for Steam login)
5. Configure `CSRF_COOKIE_SECURE=True` and `SESSION_COOKIE_SECURE=True`
6. Collect static files: `python manage.py collectstatic`
7. Set up a reverse proxy (nginx/Apache)

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/academy-csgo/static_root/;
    }

    location /uploads/ {
        alias /path/to/academy-csgo/uploads/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Troubleshooting

### "Error Fetching SteamID"
- Check `STEAM_API_KEY` is set correctly
- Ensure the Steam profile URL format is valid
- Check console logs for detailed error messages

### Database Connection Errors
- Verify MySQL is running: `docker ps` or check MySQL service
- Check `DB_DEFAULT_URL` format: `mysql://user:pass@host:port/dbname`
- For stats databases, verify the encrypted URL in Server admin

### Steam Login Not Working
- Steam login requires HTTPS in production
- Verify `STEAM_API_KEY` is valid
- Check `SITE_URL` matches your actual domain

## License

Open Source - See LICENSE file for details.
