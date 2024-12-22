# Organizations api

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

``` git clone git@github.com:asseylumva/organizations_api.git ``` 

``` cd organizations_api/ ```

Выполнить миграции

```
python3 manage.py migrate
```

Запустить dev server

```
python3 manage.py runserver
```

Api будет доступно по ссылке:

```
http://localhost:8000/api/
```
Админ панель:
```
http://localhost:8000/admin/
```
Для тестирования api создана postman коллекция в файле:
```
organizations_api.postman_collection.json
```

### В API доступны следующие эндпоинты:

* ```/api/auth/users/```  Get-запрос – получение списка пользователей. POST-запрос – регистрация нового пользователя.

* ```/api/users/{id}/``` GET-запрос – персональная страница пользователя с указанным id.

* ```/api/users/me/``` GET-запрос – страница текущего пользователя. PATCH-запрос – редактирование собственной страницы. 

* ```/api/users/set_password/``` POST-запрос – изменение собственного пароля. Доступно авторизированным пользователям.

* ```/api/auth/jwt/create/``` POST-запрос – получение токена. Используется для авторизации по емейлу и паролю, чтобы далее использовать токен при запросах.

* ```/api/auth/jwt/refresh/``` POST-запрос – обновление токена.

* ```/api/auth/jwt/verify/``` POST-запрос – проверка токена.

* ```/api/organizations/``` GET-запрос - список всех организаций. POST-запрос – создание организации.

Так же доступна документация по ссылке:

```/api/v1/docs/```