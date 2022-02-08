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

Training from: https://medium.com/django-rest/django-rest-framework-jwt-authentication-94bee36f2af8

```
~/development/fullstack-auth-django-react/backend$ python3 -m venv venv
~/development/fullstack-auth-django-react/backend$ source venv/bin/activate
(venv) ~/development/fullstack-auth-django-react/backend$ pip install django djangorestframework psycopg2-binary djangorestframework-simplejwt django-cors-headers
(venv) ~/development/fullstack-auth-django-react/backend$ django-admin startproject fullstack_auth
(venv) ~/development/fullstack-auth-django-react/backend/fullstack_auth$ python manage.py startapp auth
```

```
settings.py
    from datetime import timedelta

    INSTALLED_APPS = [
        'rest_framework',
        'rest_framework_simplejwt', if localizations/translations needed
        'corsheaders',
        -- 'auth' DO NOT ADD auth as we will use 'django.contrib.auth',
    ]

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
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

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ],
    }


    SIMPLE_JWT = {
        'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
        'ROTATE_REFRESH_TOKENS': True,
    }

    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
    ]

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
urls.py
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

### Postman - Login to get tokens

```
POST http://127.0.0.1:8000/auth/login/
Header:
    No Auth

Body:
    username: fullstackauth
    password: fullstackauth

Result:
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0NDE4ODE1MywiaWF0IjoxNjQ0MTAxNzUzLCJqdGkiOiI0YmYyM2Q1MWQxMTE0NmM2OWQ5MzBlNzM4NzFkNTljNSIsInVzZXJfaWQiOjEsInVzZXJuYW1lIjoiZnVsbHN0YWNrYXV0aCJ9.9gOxe13wEmr5czeb2xy79Pkp07L3stVzfZoogni05RM",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ0MTAyMDUzLCJpYXQiOjE2NDQxMDE3NTMsImp0aSI6ImUzYWUxYjQ1NzU0MzQxM2Y4NmMxYWNhMzc1YTQ5YzE3IiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJmdWxsc3RhY2thdXRoIn0.5hSdBrotZtKtzmdiuT0ALNZvuS5wjBjI6Aa9ohSuZpA"
    }
```

### Postman - Refresh tokens

```
POST http://127.0.0.1:8000/auth/refresh/
Headers:
    Authorization: Bearer "access token"
    Content-Type: application/json

Body:
    raw
    {
        "refresh": "refresh token",
    }

Result:
    {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ0MTc3NjE2LCJpYXQiOjE2NDQxNzcwNDAsImp0aSI6IjhiYjFmYWE3ZWFlNzQyNjI5ZGU3NTZjZTZmODRjZWQyIiwidXNlcl9pZCI6MX0.rIN3UcmzCAP88ciBWFw2-8ZTuQ5a00MvXRJv65YltuM",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0NTQ3MzMxNiwiaWF0IjoxNjQ0MTc3MzE2LCJqdGkiOiI1NGMyOTM5YTMwZjQ0MGQ2OThiMmI5NjNjYzY0YjkyMCIsInVzZXJfaWQiOjF9.6iRfNFlTvx35KSIGI0HpqCcZzWGaoKoeRP2UDlrpYe0"
    }
```

### Register User

```
auth/serializers.py
    from rest_framework import serializers
    from django.contrib.auth.models  import User
    from rest_framework.validators import UniqueValidator
    from django.contrib.auth.password_validation import validate_password

    class RegisterSerializer(serializers.ModelSerializer):
        email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
        password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
        password2 = serializers.CharField(write_only=True, required=True)

        class Meta:
            model = User
            fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
            extra_kwargs = {
                'first_name': {'required': True},
                'last_name': {'required': True}
            }

        def validate(self, attrs):
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError({'password': 'Password fields did not match.'})
            return attrs

        def create(self, validated_data):
            user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
            )

            user.set_password(validated_data['password'])
            user.save()

            return user
```

```
auth/views.py
    from .serializers import RegisterSerializer
    from rest_framework import generics
    from django.contrib.auth.models import User

    class RegisterView(generics.CreateAPIView):
        queryset=User.objects.all()
        serializer_class = RegisterSerializer
        permission_classes= (AllowAny,)
```

```
auth/urls.py
from .views importRegisterView

urlpatterns = [
   path('register/', RegisterView.as_view(), name='auth_register'),
]
```

### Postman - Register a new user

```
POST http://127.0.0.1:8000/auth/register/
Headers:
    No Auth

Body:
    username: fullstackauth1
    password: fullstackauth1
    password2: fullstackauth1
    email: fullstackauth1@fullstackauth1.com
    first_name: fullstack
    last_name: auth1

Result:
   {
        "username": "fullstackauth1",
        "email": "fullstackauth1@fullstackauth1.com",
        "first_name": "fullstack",
        "last_name": "auth1"
    }
```

### Change Password

```
auth/serializers.py
    class ChangePasswordSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
        password1 = serializers.CharField(write_only=True, required=True)
        old_password = serializers.CharField(write_only=True, required=True)

        class Meta:
            model = User
            fields = ('old_password', 'password', 'password1')

        def validate(self, attrs):
            if attrs['password'] != attrs['password1']:
                raise serializers.ValidationError({'password': 'Password fields did not match.'})
            return attrs

        def validate_old_password(self, value):
            user = self.context['request'].user
            if not user.check_password(value):
                raise serializers.ValidationError({'old_password': 'Old password is not correct'})
            return value

        def update(self, instance, validated_data):
            user = self.context['request'].user
            if user.pk != instance.pk:
                raise serializers.ValidationError({'authorize': "You don't have permission for this user."})

            instance.set_password(validated_data['password'])

            return instance
```

```
auth/views.py
    from rest_framework.permissions import IsAuthenticated

    class ChangePasswordView(generics.UpdateAPIView):
        queryset=User.objects.all()
        serializer_class = ChangePasswordSerializer
        permission_classes = (IsAuthenticated,)
```

```
auth/urls.py
    from .views import ChangePasswordView

    urlpatterns = [
        path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='change_password'),
    ]
```

### Postman - Change password

```
PUT http://127.0.0.1:8000/auth/change_password/1/
Headers:
    Authorization: Bearer "access token"
    Content-Type: application/json

Body:
    password: new_fullstackauth
    password2: new_fullstackauth
    old_password: fullstackauth # because no filter for a specific user yet

Result:
    {}
```

### Update Profile

```
auth/serializers.py
    class UpdateUserSerializer(serializers.ModelSerializer):
        email = serializers.EmailField(required=True)

        class Meta:
            model = User
            fields = ('username', 'first_name', 'last_name', 'email')
            extra_kwargs ={
                'first_name': {'required': True},
                'last_name' : {'required': True},
            }

        def validate_email(self, value):
            user = self.context['request'].user
            if User.objects.exclude(pk=user.pk).filter(email=value).exists():
                raise serializers.ValidationError({'email': 'This email is already in use.'})

            return value

        def validate_username(self, value):
            user = self.context['request'].user
            if User.objects.exclude(pk=user.pk).filter(username=value).exists():
                raise serializers.ValidationError({'user': 'This user name is already in use.'})

            return value

        def update(self, instance, validated_data):
            user = self.context['request'].user

            if user.pk != instance.pk:
                raise serializers.ValidationError({'authorize': "You don't have permission for this user."})

            instance.first_name = validated_data['first_name']
            instance.last_name = validated_data['last_name']
            instance.email = validated_data['email']
            instance.username = validated_data['username']

            instance.save()
            return instance

```

```
auth/views.py
    from .serializers import UpdateUserSerializer

    class UpdateUserView(generics.UpdateAPIView):
        queryset=User.objects.all()
        serializer_class = UpdateUserSerializer
        permission_classes = (IsAuthenticated,)
```

```
from .views import UpdateUserView

urlpatterns = [
    path('update_user/<int:pk>/', UpdateUserView.as_view(), name='auth_update_user')
]
```

### Postman - Update user profile

```
PUT http://127.0.0.1:8000/auth/update_user/1/
Headers:
    Authorization: Bearer "access token"
    Content-Type: application/json

Body:
    username: new_fullstackauth
    first_name: new_fullstack
    last_name: new_auth
    email: new_fullstack@fullstackauth.com

Result:
    {
        "username": "new_fullstackauth",
        "first_name": "new_fullstack",
        "last_name": "new_auth",
        "email": "new_fullstack@fullstackauth.com"
    }
```

### Logout

```
INSTALLED_APPS = [
    'rest_framework_simplejwt.token_blacklist',
]
```

```
(venv) ~/development/fullstack-auth-django-react/backend/fullstack_auth$ python manage.py makemigrations
(venv) ~/development/fullstack-auth-django-react/backend/fullstack_auth$ python manage.py migrate

```

Cron job for blacklist's flushexpiredtokens: delete any tokens from the outstanding list and blacklist that have expired

Blacklist not compatible with custom fields (MyTokenObtainPairSerializer) --> Default view TokenObtainPairSerializer is needed

```
auth/urls.py
    from .views import TokenObtainPairView # MyTokenObtainPairView, custom field not supported by blacklist

    urlpatterns = [
        path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    ]
```

```
auth/views.py
    from rest_framework_simplejwt.tokens import RefreshToken
    from rest_framework.views import APIView
    from rest_framework.response import Response
    from rest_framework import status

    class LogoutView(APIView):
        permission_classes = (IsAuthenticated,)

        def post(self, request):
            try:
                refresh_token = request.data['refresh']
                token = RefreshToken(refresh_token)
                token.blacklist()

                return Response(status=status.HTTP_205_REST_CONTENT)
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)

```

```
auth/urls.py
    from .views import LogoutView

    urlpatterns = [
        path('logout/', LogoutView.as_view(), name='auth_logout')
    ]
```

```
Scenario 1
    SIMPLE_JWT = {
        'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
        'ROTATE_REFRESH_TOKENS': True,
        'BLACKLIST_AFTER_ROTATION': True
    }

    Login: refresh token --> + outstanding tokens automatically
    Logout: refresh token --> + blacklisted tokens manually
    Refresh: old refresh token --> + blacklisted tokens automatically
            new refresh token --> + outstanding tokens manually
```

```
Scenario 2
    SIMPLE_JWT = {
        'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
        'ROTATE_REFRESH_TOKENS': True,
        'BLACKLIST_AFTER_ROTATION': False
    }

    Login: refresh token --> + outstanding tokens automatically
    Logout: refresh token --> + blacklisted tokens manually
    Refresh: old refresh token --> + blacklisted tokens manually
            new refresh token --> + outstanding tokens manually
```

```
Scenario 3
    SIMPLE_JWT = {
        'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
        'ROTATE_REFRESH_TOKENS': False,
        'BLACKLIST_AFTER_ROTATION': False
    }

    Login: refresh token --> + outstanding tokens automatically
    Logout: refresh token --> + blacklisted tokens manually
    Refresh: no actions
```

```
auth/views.py
    class LogoutAllView(APIView):
        permission_classes = (IsAuthenticated,)

        def post(self, request):
            tokens = OutstandingToken.objects.filter(user_id=request.user.id)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)

            return Response(status=status.HTTP_205_RESET_CONTENT)
```

```
auth/urls.py
    from .views import LogoutAllView
    urlpatterns = [

        path('logout_all', LogoutAllView.as_view(), name='auth_logout_all')
    ]
```

### Postman - Login to get tokens

```
POST http://127.0.0.1:8000/auth/login/
Headers:
    No Auth
Body:
    username: fullstackauth
    password: fullstackauth

Result:
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0NTQ3MzA0MCwiaWF0IjoxNjQ0MTc3MDQwLCJqdGkiOiJhMDM4ZjE1Yjg2Y2Y0NjIzOWI2OTgyZTI1OGEyODM4YiIsInVzZXJfaWQiOjF9.wpf9-0Naa4nYUMxHIdDjBFoW8r2nBOrxQAAoxaIbZYE",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ0MTc3MzQwLCJpYXQiOjE2NDQxNzcwNDAsImp0aSI6IjgwY2U2ZjMxMzM3MTRlMGVhZjA0MjgwZjY0ZDI5NmQ5IiwidXNlcl9pZCI6MX0.LA_5iu_qDs7YIU4PngzMkTmQ-S6JORM_GMmWjFwqUys"
    }
```

### Postman - Logout to add a refresh token to blacklist

```
POST http://127.0.0.1:8000/auth/logout/
Headers:
    Authorization: Bearer "access token"
    Content-Type: application/json

Body:
    raw
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0NTQ3MzA0MCwiaWF0IjoxNjQ0MTc3MDQwLCJqdGkiOiJhMDM4ZjE1Yjg2Y2Y0NjIzOWI2OTgyZTI1OGEyODM4YiIsInVzZXJfaWQiOjF9.wpf9-0Naa4nYUMxHIdDjBFoW8r2nBOrxQAAoxaIbZYE",
    }

Result:
    {}
```

### Postman - Test using refresh token blacklisted

```
POST  http://127.0.0.1:8000/auth/login/refresh/
Headers:
    Authorization: Bearer "access token"
    Content-Type: application/json

Body:
    raw
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0NTQ3NDExMywiaWF0IjoxNjQ0MTc4MTEzLCJqdGkiOiJjYTg1YWJlMzNiYTQ0ZGJlYjgxYWJkMGQxYjMxMDBjNSIsInVzZXJfaWQiOjF9.Lg1yJjPqyyAJbDmkd8mTPmF7Ff0MrcoV0e8U2nmJHcA"
    }

Result:
    {
        "detail": "Token is blacklisted",
        "code": "token_not_valid"
    }
```

### Postman - Log out all tokens

```
POST   http://127.0.0.1:8000/auth/logout_all/
Headers:
    Authorization: Bearer "access token"
    Content-Type: application/json

Result:
    {}
```

### Error

[06/Feb/2022 20:10:34] "POST /auth/login/refresh/ HTTP/1.1" 401 58

https://stackoverflow.com/questions/70761933/how-to-solve-error-401-unauthorized-login-in-drf-simple-jwt-user-login

### Frontend - React

```
~/development/fullstack-auth-django-react$ sudo npm install -g create-react-app
~/development/fullstack-auth-django-react$ npx create-react-app frontend
~/development/fullstack-auth-django-react$ cd frontend
~/development/fullstack-auth-django-react/frontend$ npm start
~/development/fullstack-auth-django-react/frontend$ npm install @mui/material @emotion/react @emotion/styled @mui/icons-material axios react-cookie react-router-dom@6

```
Auto format: Shift + Alt + F

### SignIn - Dummy Page
``` js
components/SignIn.js
    import React from 'react';

    const SignIn = () => {
        return (
            <div>
                <h1> Sign In </h1>
            </div>
        )
    };

    export default SignIn;
```

### Profile - Dummy Page
``` js
components/Profile.js
    import React from 'react';

    const Profile = () => {
        return (
            <div>
                <h1> Profile </h1>
            </div>
        )
    };

    export default Profile;
```

### Route Pages
``` js
index.js
    import { BrowserRouter } from 'react-router-dom';

    ReactDOM.render(
    <React.StrictMode>
        <BrowserRouter>
            <App />
        </BrowserRouter>
    </React.StrictMode>,
    document.getElementById('root')
    );    
```

``` js
App.js
    function App() {
        return (
            <div className="App">
                <h1>Fullstack Auth Django React </h1>
                <Routes>
                    <Route path='/' element={<SignIn/>} />
                    <Route path='profile' element={<Profile/>}/>
                </Routes>
            </div>
        );
    }
```

### Sign In

``` js
components/SignIn.js
https://github.com/mui/material-ui/blob/master/docs/data/material/getting-started/templates/sign-in/SignIn.js

    import {
        Avatar,
        Box,
        Button,
        Checkbox,
        Container,
        createTheme,
        CssBaseline,
        FormControlLabel,
        Grid,
        Link,
        TextField,
        ThemeProvider,
        Typography
        } from '@mui/material';
    import LockOutlinedIcon from '@mui/icons-material/LockOutlined';

    const Copyright = (props) => {
        return (
            <Typography variant="body2" color="text.secondary" align="center" {...props}>
            {"Copyright ©"}
            <Link color="inherit" href="#">
                Tae Hee Choi
            </Link>{' '}
            {new Date().getFullYear()}
            {"."}
            </Typography>
        )
    }

    const theme = createTheme()

    const SignIn = () => {
    const handleSubmit = (e) => {
        e.preventDefault()
        const data = new FormData(e.currentTarget);
        // eslint-disable-next-line no-console
        console.log({
        email: data.get('email'),
        password: data.get('password'),
        });
    }
    return (
        <ThemeProvider theme={theme}>
        <Container component="main" maxWidth="xs">
            <CssBaseline />
            <Box
            sx={{
                marginTop: 8,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center'
            }}
            >
            <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                <LockOutlinedIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
                Sign In
            </Typography>
            <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                <TextField
                margin="normal"
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                autoComplete="email"
                autoFocus
                />
                <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="password"
                type="password"
                id="password"
                autoComplete="current-password"
                />
                <FormControlLabel
                control={<Checkbox value="remember" color="primary" />}
                label="Remember me"
                />
                <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
                >
                Sign In
                </Button>
                <Grid container>
                <Grid item xs>
                    <Link href="#" variant="body2">
                    Forgot Password?
                    </Link>
                </Grid>
                <Grid item>
                    <Link href="#" variant="body2">
                    {"Don't have an account? Sign Up"}
                    </Link>
                </Grid>
                </Grid>
            </Box>
            </Box>
            <Copyright sx={{ mt: 8, mb: 4 }} />
        </Container>
        </ThemeProvider>
    )
    };

    export default SignIn;
```

### SignIn Axios to API
``` js
components/SignIn.js
    import axios from 'axios';

    const handleSubmit = (e) => {
        e.preventDefault()
        const data = new FormData(e.currentTarget);

        axios.post(`http://127.0.0.1:8000/auth/login/`, {
            username: data.get('username'),
            password: data.get('password')
        })
        .then(res => {
            console.log(res.data);
        })
    }

{refresh: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90e…iOjF9.FnZeIgOHn_w9VLMw_wSkeAnnN3c9lFcU1k3nfw4BH1k', access: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90e…I6MX0.ZKhMb6635NvJSu0WleMg3V2vJ4WYTRlKhdV5wkdAgIA'}
```

### Token to Cookies and Navigate to Profile
``` js
index.js
    import { CookiesProvider } from 'react-cookie';

    ReactDOM.render(
        <React.StrictMode>
            <CookiesProvider>
                <BrowserRouter>
                    <App />
                </BrowserRouter>
            </CookiesProvider>
        </React.StrictMode>,
    document.getElementById('root')
    );
```

``` js
components/SignIn.js
    import { useCookies } from 'react-cookie';
    import { useNavigate } from 'react-router-dom';
    
    let navigate = useNavigate()

    const [cookies, setCookies] = useCookies(['user'])

    const handleSubmit = (e) => {
        e.preventDefault()
        const data = new FormData(e.currentTarget);

        axios.post(`http://127.0.0.1:8000/auth/login/`, {
            username: data.get('username'),
            password: data.get('password')
        })
        .then(res => {
            setCookies('access', res.data.access, {path: '/'}) //# path:'/' signifies that the cookie is available for all the pages of the website
            setCookies('refresh', res.data.refresh, {path: '/'})
            navigate('/profile')
        })
    }
```

https://dev.to/cotter/localstorage-vs-cookies-all-you-need-to-know-about-storing-jwt-tokens-securely-in-the-front-end-15id


https://www.robinwieruch.de/react-hooks-fetch-data/