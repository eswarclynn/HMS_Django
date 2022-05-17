## Hostel Management System - National Institute of Technology, Andhra Pradesh

A hostel management system for paperless and reliable management of hostels. To be deployed at the Hostels of National Institute of Technology, Andhra Pradesh.

Hosted at: http://hmsepc.herokuapp.com/

### Dev Environment Setup - Windows: 

**Requires python and pip**

#### Setup Django and python packages(CMD/Terminal at PreferredDirectory)
 - `git clone https://github.com/Deepzzz54321/HMS_Django.git`
 - `cd HMS_Django`
 - `python -m venv myvenv`
 - `myvenv/Scripts/activate`
 - `pip install -r requirements.txt`
 - Create .env file inside HMS_Django/hosteldb with:
```
SECRET_KEY=&54=+66-wt)d319m09du8+((^lb+-(m4r1bi&&^fgv7@u6+6h6
DEBUG=True
ENVIRONMENT=development
APP_EMAIL=<placeholder_email>
APP_EMAIL_PASSWORD=<placeholder_email_password>
```
Key generated at https://miniwebtool.com/django-secret-key-generator/

#### Setup PostgreSQL DB(in psql cli)
- Install PostgreSQL following https://www.postgresqltutorial.com/postgresql-getting-started/install-postgresql/.
- Run `psql` or `psql postgres`(whichever works) in your terminal and run the following commands.
  - `CREATE DATABASE hosteldb;`
  - `CREATE USER hosteladmin WITH PASSWORD 'hostel123';`
  - `ALTER ROLE hosteladmin SET client_encoding TO 'utf8';`
  - `ALTER ROLE hosteladmin SET default_transaction_isolation TO 'read committed';`
  - `GRANT ALL PRIVILEGES ON DATABASE hosteldb TO hosteladmin;`
- Update whatever password you choose in `settings.py`.


#### Migrate, Create Superuser and Run Server(CMD/Terminal at PreferredDirectory/HMS_Django)
 - `python manage.py migrate`
 - `python manage.py createsuperuser`
 - Fill in required details
 - `python manage.py runserver`
 - Visit **http://localhost:8000/admin** and login using the previously entered credentials.
 - Create Officials, Students and Blocks.
 - Visit **http://localhost:8000/** in another browser window and Sign Up with any of the previously entered emails of Officials or Students.
 - On sign up verification link will be sent through mail in production, in development visit the CMD/Terminal where you ran `python manage.py runserver` to find the verification link and open it in the browser.
 - Login using the credentials previously used to sign up.
