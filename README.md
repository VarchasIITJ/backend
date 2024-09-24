# Varchas ![Status active](https://img.shields.io/badge/Status-active%20development-2eb3c1.svg) ![Django 4.2.7](https://img.shields.io/badge/Django-4.2.7-green.svg) ![Python 3.12.5](https://img.shields.io/badge/Python-3.12.5-blue.svg) ![Python Package CI](https://github.com/devlup-labs/varchas/workflows/Python%20package/badge.svg)

## Main web portal for the annual sports fest of IIT Jodhpur Varchas.

### Installation:

Requirements:

- Python 3.12.5
- Django 4.2.7
- Other dependencies in `requirements.txt`

Procedure:

- Install [python](https://www.python.org/downloads/) in your environment(pre-installed on Ubuntu).
- Navigate to the cloned repository.
  ```
  cd <project_directory_name>     # varchas_iitj
  ```
- Install `pipenv` for dependency management
  ```
  pip install pipenv
  ```
- Use pip to install other dependencies from `requirements.txt`

  ```
  pip install -r requirements.txt
  ```

- Optionally activate virtual environment, if you don't want to activate env, use `pipenv run` to run python scripts

  ```
  source "$(pipenv --venv)"/bin/activate
  ```

- Make database migrations
  ```
  python manage.py makemigrations
  python manage.py migrate
  ```
  NOTE: If its your first time migrating, you may need to manually add migration module in each app.
  ```
  python manage.py makemigrations main
  python manage.py makemigrations accounts
  python manage.py makemigrations adminportal
  python manage.py makemigrations events
  python manage.py makemigrations registration
  python manage.py makemigrations sponsors
  python manage.py makemigrations app_apis
  python manage.py migrate
  ```
- Create a superuser
  ```
  python manage.py createsuperuser
  ```
- Run development server on localhost
  ```
  python manage.py runserver
  ```
