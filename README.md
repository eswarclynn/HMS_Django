# Hostel Management System - Django

Clone the project to your local system

```git clone https://github.com/Deepzzz54321/HMS_Django.git```

Create a virtual environment inside the cloned directory

```python -m venv myvenv```

Activate the virtual Environment

```myvenv\Scripts\activate```

Install Requirements

```pip install -r requirements.txt```

## Database Configuration

Create 'hosteldb' database

```
CREATE SCHEMA IF NOT EXISTS `hosteldb`;
USE `hosteldb` ;
```
Create an authentication user and grant privileges to this user.
```
CREATE USER 'hosteladmin'@'localhost:3306' IDENTIFIED WITH mysql_native_password ‘12345’;
grant all on djangodatabase.* to ‘hosteladmin’@’%’;
flush privileges;
```

## Django Configuration

Install MySQLClient through CLI
```
pip install mysqlclient-1.4.6-cp38-cp38-win32.whl
```
Open the settings.py file of the Django project. Change ```DATABASES = ``` to
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hosteldb',
        'USER': 'hosteladmin',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
Migrate and create new superuser(admin) by providing eMail and password using CLI
```
python manage.py migrate
python manage.py createsuperuser
```
Initially the database is empty. Populate it with students in Institutestd, staff in Officials, blocks in Blocks as your wish using the

Make migrations and migrate again
```
python manage.py makemigrations
python manage.py migrate
```
That's it. Your local server is ready to run!
```
python manage.py runserver
```

### IMPORTANT
Initially the database is empty. Populate it with students in Institutestd, staff in Officials, blocks in Blocks as your wish using the django admin interface at ```http://localhost:8000/admin/``` and login using the credentials of the superuser you created.
After populating the database, use them to test the system.

Your Hostel Management System is ready to go!
