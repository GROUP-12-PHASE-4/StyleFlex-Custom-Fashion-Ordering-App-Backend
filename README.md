# STYLEFLEX-BACKEND
This is the backend for the StyleFlex Custom Fashion Ordering App..It provides RESTful API endpoints for user authentication, managing designs, handling orders,and user profiles.

## FEATURES
- User Authentication(JWT)
- CRUD operations for fashion designs 
- Create and track orders
- Admin-only Routes for mananging orders
- User profile update support 

## TECH STACK
- Python 3.11+
- Flask 
- Flask-migrate
- Flask-SQL-Alchemy
- Flask-JWT-Extended
- PostgreSQL

## SETUP INSTRUCTIONS 
### 1. Clone the repository
- git clone https://github.com/your-username/styleflex-backend.git
- cd styleflex-backend

### 2. Create and actiavte a virtual environment
- pipenv install
- pipenv shell

### 3. Install Dependencies
- pip install -r requirements.txt

### 4. Setup environmental variables
- FLASK_APP=app
- FLASK_ENV=development
- DATABASE_URL=postgresql://<username>:<password>@localhost:5432/styleflex_db
- SECRET_KEY=your-secret-key
- JWT_SECRET_KEY=your-jwt-secret

## RUNNING THE APP
### INitialize the database 
- flask db init
- flask db migrate -m "Initial migration"
- flask db upgrade
### Running the development server
- flask run

## AUTHENTICATION
- POST/auth/register- Creates new user 
- POST/auth/login- Returns access token 
- Use token in protected routes with:
- Authorization: Bearer <your_token>


## POSTGRESQL SETUP(LOCAL)
createdb styleflex_db (make sure to match this with your DATABASE_URL)

## DEPLOYMENT
(e.g on render)
### Build command 
pip install -r requirements.txt
### Start Command
gunicorn app:app
### Environment Variables (in Render dashboard):
- FLASK_ENV=production
- SECRET_KEY=your-secret
- JWT_SECRET_KEY=your-jwt-secret
- DATABASE_URL=your-render-postgresql-url


## PROJECT STRUCTURE
``` plaintext
styleflex-backend/
├── app.py                       # App entry point
├── database.py                  # SQLAlchemy setup
├── models.py                    # Database models
├── utils.py                     # Helper functions (e.g., decorators)
├── routes/                      # Flask blueprints
│   ├── __init__.py
│   ├── auth_routes.py
│   ├── design_routes.py
│   └── order_routes.py
├── migrations/                  # Flask-Migrate files
│   └── versions/
├── seed.py                      # Seed data script
├── seed_admin.py                # Seed admin account
├── init_db.py                   # Optional database init script
├── .env                         # Environment variables (not committed)
├── requirements.txt             # Python dependencies
├── Procfile                     # For Render deployment
├── README.md                    # Project documentation
└── venv/                        # Virtual environment (excluded in .gitignore)

```
## LICENESE
MIT 
### ACKNOWLEDGEMENTS
```
- ELAINE BUYEKE
- STACEY TAREI
- LEWIS NJUMA
- BILLADAMS NYAMWENO
