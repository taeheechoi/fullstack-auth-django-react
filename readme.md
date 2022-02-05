### Configure VS Code for Django
https://code.visualstudio.com/docs/python/tutorial-django

Interpreter (Ctrl+Shift+P) ./backend/venv/bin/python3

Debugger. Add configure. 
```
    "configurations": [
        {
            "name": "Python: Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/backend/fullstack_auth/manage.py",
            "args": [
                "runserver"
            ],
            "django": true
        }
    ]
}

```

### Database - Postgres
docker-compose.yml
```
    version: '3.1'

    services:

    db:
        image: postgres
        restart: always
        environment:
        POSTGRES_PASSWORD: example
        ports:
        - 5432:5432
        volumes:
        - db-data:/var/lib/postgresql/data

    adminer:
        image: adminer
        restart: always
        ports:
        - 8080:8080

    volumes:
    db-data:
        driver: local

```
```
~/development/fullstack-auth-django-react$ docker-compose up -d
~/development/fullstack-auth-django-react$ docker ps

http://localhost:8080/
system: PostgreSQL
server: db
username: postgres
password: example
```

```
    CREATE DATABASE fullstackauth;

    CREATE USER fullstackauth WITH PASSWORD 'fullstackauth' CREATEDB;

    SELECT usename AS role_name,
    CASE 
        WHEN usesuper AND usecreatedb THEN 
        CAST('superuser, create database' AS pg_catalog.text)
        WHEN usesuper THEN 
            CAST('superuser' AS pg_catalog.text)
        WHEN usecreatedb THEN 
            CAST('create database' AS pg_catalog.text)
        ELSE 
            CAST('' AS pg_catalog.text)
    END role_attributes
    FROM pg_catalog.pg_user
    ORDER BY role_name desc;

```

### Backend - Django 
```
~/development/fullstack-auth-django-react/backend$ python3 -m venv venv
~/development/fullstack-auth-django-react/backend$ source venv/bin/activate
(venv) ~/development/fullstack-auth-django-react/backend$ pip install django djangorestframework psycopg2-binary djangorestframework-simplejwt
(venv) ~/development/fullstack-auth-django-react/backend$ django-admin startproject fullstack_auth
(venv) ~/development/fullstack-auth-django-react/backend/fullstack_auth$ python manage.py startapp auth
```

```
settings.py
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        -- 'auth' DO NOT ADD auth as we will use 'django.contrib.auth',
    ]

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'fullstackauth',
            'USER': 'fullstackauth',
            'PASSWORD': 'fullstackauth',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }

```

```
(venv) ~/development/fullstack-auth-django-react/backend/fullstack_auth$ python manage.py createsuperuser 
ID: fullstackauth
PW: fullstackauth
```

### Login User
```
auth/serializers.py
    from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

    class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

        @classmethod
        def get_token(cls, user):
            token = super(MyTokenObtainPairSerializer, cls).get_token(user)

            token['username'] = user.username

            return token
```

```
auth/views.py
    from .serializers import MyTokenObtainPairSerializer
    from rest_framework_simplejwt.views import TokenObtainPairView
    from rest_framework.permissions import AllowAny

    class MyTokenObtainPairView(TokenObtainPairView):
        serializer_class = MyTokenObtainPairSerializer
        permission_classes = (AllowAny,)

```

```
uils.py
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('auth/', include('auth.urls'))
    ]
```

```
auth/urls.py
    from django.urls import path
    from .views import MyTokenObtainPairView
    from rest_framework_simplejwt.views import TokenRefreshView

    urlpatterns = [
        path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('login/refresh', TokenRefreshView.as_view(), name='token_refresh' )
    ]
```

### Postman
```
POST http://127.0.0.1:8000/auth/login/
No Auth,
username: fullstackauth
password: fullstackauth
```

```
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0NDE4ODE1MywiaWF0IjoxNjQ0MTAxNzUzLCJqdGkiOiI0YmYyM2Q1MWQxMTE0NmM2OWQ5MzBlNzM4NzFkNTljNSIsInVzZXJfaWQiOjEsInVzZXJuYW1lIjoiZnVsbHN0YWNrYXV0aCJ9.9gOxe13wEmr5czeb2xy79Pkp07L3stVzfZoogni05RM",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ0MTAyMDUzLCJpYXQiOjE2NDQxMDE3NTMsImp0aSI6ImUzYWUxYjQ1NzU0MzQxM2Y4NmMxYWNhMzc1YTQ5YzE3IiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJmdWxsc3RhY2thdXRoIn0.5hSdBrotZtKtzmdiuT0ALNZvuS5wjBjI6Aa9ohSuZpA"
    }
```
### Register User 