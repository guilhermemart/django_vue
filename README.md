# django_vue
    Estrutura do projeto
        django_vue
            |
            |-backend --> python -m django startproject backend .
            |   |-app_django --> cd backend | python -m django startapp app_django
            |   |-urls.py << aqui o axios vai buscar as urls
            |   |-settings.py
            |   |-others.py
            |   |-.env --> crie/edite isso na sua maquina
            |
            |-frontend
            |   |-app vue
            |      |-.env --> crie/edite isso na sua maquina localmente
            |
            |-manage.py
    
* Usage:
    - clone
    - edite o .env do backend e o .env do frontend ask manteiners for the keys
* Instale o postgresql
    - no terminal
      * sudo apt install libpq-dev python-dev postgresql postgresql-contrib
* Crie um database e um user
    - no terminal
      * sudo su - postgres
      * psql  << entrar no shell do pg
      * CREATE DATABASE altave;  << nao esquecer o ";"
      * CREATE USER  altave WITH PASSWORD 'altave';
      * ALTER ROLE altave SET client_encoding TO 'utf8';
      * ALTER ROLE altave SET default_transaction_isolation TO 'read committed';
      * GRANT ALL PRIVILEGES ON DATABASE altave TO altave;
      * \q
      * exit
  
* Configure o Django database no settings.py
    - Vai estar assim:
      
          . . .
          
          DATABASES = {
              'default': {
                  'ENGINE': 'django.db.backends.sqlite3',
                  'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
              }
          }
          
          . . .
    - Faça ficar assim:
      
          . . .
            
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql_psycopg2',
                    'NAME': 'altave',
                    'USER': 'altave',
                    'PASSWORD': 'altave',
                    'HOST': 'localhost',
                    'PORT': '',
                }
            }
            
            . . .
* Crie as migraçoes do django:
    - cd django_vue 
    - python -m manage makemigrations
    - python -m manage migrate
* Crie um superusuario
    - python -m manage createsuperuser

* Rode o django
  - python -m manage runserver

* Rode o vue:
  - cd django_vue/frontend
  - npm install  
  - npm run serve
    
* Manteiners:
    - Guilherme Martins
    - Celso Reis