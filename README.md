# STYLEFLEX-BACKEND
This is the backend for the StyleFlex Custom Fashion Ordeing App..It provides RESTful API endpoints for user authentication, managing designs, handling orders,and user profiles.

## FEATURES
-User Authentication(JWT)
-CRUD for fashion designs 
-Create and track orders
-Admin-ONly Routes for mananging orders
-Profile update support 

## TECH STACK
-Python 3.11+
-flask 
-Flask-migrate
-Flask-SQL-Alchemy
-Flask-JWT-Extended
-PostgreSQL

## SETUP INSTRUCTIONS 
### 1. Clone the repository
git clone https://github.com/your-username/styleflex-backend.git
cd styleflex-backend

### 2. Create and actiavte a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Setup environmental variables
FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/styleflex_db
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

## RUNNING THE APP
### INitialize the database 
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
### Running the development server
flask run

## AUTHENTICATION
POST/signup - Creates new user 
POST/login- Returns access token 
Use token in protected routes with:
Authorization: Bearer <your_token>


## POSTGRESQL SETIP(LOCAL)
createdb styleflex_db (make sure to match this with your DATABASE_URL)

## DEPLOYMENT
(e.g on render)
### Build command 
pip install -r requirements.txt
### Start Command
gunicorn app:app
### Environment Variables (in Render dashboard):
FLASK_ENV=production
SECRET_KEY=your-secret
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=your-render-postgresql-url

## LICENSE 
MIT © 2025 StyleFlex

## ACKNOWLEDGEMENTS
BILLY ADAMS
ELAINE BUYEKE
STACEY TAREI
LEWIS



