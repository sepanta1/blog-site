# Django Blog Website

A full-featured blog website built using the Django framework.
This project is a personal blog application developed with Django.
It utilizes a ready-made frontend template for the user interface and leverages many of Django's built-in features, such as authentication, admin panel, and ORM. Additionally, it integrates useful third-party packages to enhance functionality.

## Features

*  User authentication (register, login, logout)
*  Blog post CRUD (create, read, update, delete)
*  Rich text editor using TinyMCE
*  Categories and tags (django‑taggit)
*  Comment system on posts
*  Contact form
*  Django Admin customization
*  CAPTCHA protection in admin
*  SEO helpers (robots.txt, sitemaps)
*  Separate development & production settings
*  Environment variable–based secrets

## Technologies Used

*  Backend: Django (Python)
*  Frontend: HTML, CSS, JavaScript (with Bootstrap)
*  Database: SQLite (default) or PostgreSQL in production
*  Third-party packages: TinyMCE, Django Taggit,Django Simple Captcha

## Installation
1. Clone the repository:
```
git clone https://github.com/sepanta1/blog-site.git
```
2. Navigate to the project directory:
```
cd blog-site
```
3. Create a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
4. Set environment variables:
```bash 
export DJANGO_ENV=dev
export DJANGO_SECRET_KEY=your-secret-key
```
5. Install dependencies:
```
pip install -r requirements.txt
```
6. Apply migrations:
```
python manage.py migrate
```
7. Create a superuser:
```
python manage.py createsuperuser
```
8. Run the development server:
```
python manage.py runserver
```
9. Visit http://127.0.0.1:8000/ in your browser.

## Usage

*  Access the admin panel at /admin/ with your superuser credentials.
*  Create posts and manage content through the interface.
## Screenshots:

## Contributing
Contributions are welcome. Please open an issue or submit a pull request.

## License
MIT License
