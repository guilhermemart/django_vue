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

* Crie as migraçoes do django:
    - cd django_vue 
    - python -m makemigrations
    - python -m migrate

* Rode o django
  - python -m manage runserver

* Rode o vue:
  - cd django_vue/frontend
  - mng run serve
    
* Manteiners:
    - Guilherme Martins
    - Celso Reis