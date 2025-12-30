# Blog Site
A full-featured blog website built using the Django framework.

## Description
This project is a personal blog application developed with Django.
It utilizes a ready-made frontend template for the user interface and leverages many of Django's built-in features, such as authentication, admin panel, and ORM. Additionally, it integrates useful third-party packages to enhance functionality.

## Screenshots

## Features

*  User registration, login, and authentication
*  Create, edit, and delete blog posts with rich text editing (TinyMCE)
*  Image uploads for posts
*  Hierarchical and threaded comment system
*  Post categorization and tagging
*  Full-text search across posts
*  Simple CAPTCHA for forms (to prevent spam)
*  Responsive design optimized for mobile and desktop
*  Built-in Django admin panel for easy content management
*  Separate settings for development and production

## Technologies Used

*  Backend: Django (Python)
*  Frontend: HTML, CSS, JavaScript (with Bootstrap)
*  Database: SQLite (default) or PostgreSQL in production
*  Third-party packages: (list specific ones used, e.g., django-ckeditor, pillow, etc.)

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
4. Install dependencies:
```
pip install -r requirements.txt
```
5. Apply migrations:
```
python manage.py migrate
```
6. Create a superuser:
```
python manage.py createsuperuser
```
7. Run the development server:
```
python manage.py runserver
```
8. Visit http://127.0.0.1:8000/ in your browser.

## Usage

*  Access the admin panel at /admin/ with your superuser credentials.
*  Create posts and manage content through the interface.

## Contributing
Contributions are welcome. Please open an issue or submit a pull request.

## License
MIT License
