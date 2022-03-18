con# django_vue
    Estrutura do projeto
        django_vue
            |
            |-backend --> python -m django startproject backend .
            |   |-app_django --> cd backend | python -m django startapp app_django
            |       |-.env --> crie/edite isso na sua maquina
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
    - Reinicie    
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
- Problema comum, erro no django por nao conseguir logar  no banco de dados ao rodar o servidor
  - solução: refaça os passos acima
  
* Configure o Django database no settings.py (no git já está ok)
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

* Instalar os requirements.txt 
    - pip install -r requirements.txt

* Verifique todos os .env's do codigo (3), o ip deve ser igual ao da maquina que está rodando o sistema

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

* Adicionar usuários não admin:
  - Entre na página de admin do Django (IP:PORT/admin/)
  - Na linha de "Usuários" clique em "+ Adicionar"
  - Crie um usuário e desmarque as permissões para ficar somente "Ativo"
    
* Configurar no oracle.py apasta que vai ser usada como deposito de imagens para as cameras realtime
* Configurar ip e porta no oracle.py
* Rodar python -m oracle.py

* Maintainers:
    - Guilherme Martins
    - Celso Reis
    - Devanir Ramos