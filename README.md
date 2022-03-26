# User-login

#### Depedency check and installtion
1. Python 3.7
2. boto3, SQLAlchemy, Flask, etc installed via `pip install -r requirements.txt`

### App directory stucture
```
|-- aws_lambda_fleet
    |-- user_app
    |   |-- app.py
    |   |-- models.py
    |   |-- schema.py
    |   |-- views.py
    |-- config.py
    |-- manage.py
    |-- routes.py
    |-- requirements.txt
```

### Migrations steps
```
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```

### Using Flask Marshmallow

To design the model schema for all the model request to support marshing and unmarshing datas, filter out fields and to Jsonify the data to server better for the RESTful API.

### Installing python dependencies
`$ pip install -r requirements.txt`

## Restful APIs

- GET/POST  `/user_app/hello` -> To test your installation and setups
- GET  `/user_app/` -> List all Users
- POST `/user_app/` -> Create new user
- POST  `/user_app/login` -> Authenticate user
- GET  `/user_app/{id}` -> Get user details with id
- PUT  `/user_app/{id}/upload_image` -> upload image

1. Say Hello World:

    GET/POST API `/user_app/hello` call to check for the flask app and user app is running into your environment or server.

    Request: GET/POST `/user_app/hello`

    Response: `{"message": "Hello, World!"}`

2. List down the users.

    GET API `/user_app/` to list out all the users accessing to this app.

    Request: GET `/user_app/`

    Response: Status code 200 OK
    ```
    {
        "status": "success",
        "data": [
            {
                "profile": "s3://bucket_name/path_to_profile_dir/unique_uuid.jpg",
                "first_name": "user_firstname",
                "id": user_id,
                "age": integer,
                "email": "user@gmail.com",
                "last_name": "user_lastname"
            },
            {
                "profile": null,
                "first_name": "user_firstname",
                "id": user_id,
                "age": integer,
                "email": "user@gmail.com",
                "last_name": "user_lastname"
            },
            ...
        ]
    }

3. Create new User:

    POST API call `/user_app/`, to create new users.

    Request: POST `/user_app/`

    Request Parameters: raw json data

    ```
    {
        "first_name":"user_firstname",
        "last_name":"user_lastname",
        "password":"user_password",  ## will not be shown in any the GET calls
        "age":"user_age",  ## optional
        "email":"user_email_address@domain_name.extension"
    }
    ```

    Response: User details with status code 201 CREATED

    ```
    {
        "status": "success",
        "data": {
            "last_name": "user_lastname",
            "id": user_unique_id,
            "profile": null,  ## user profile will be null/default untill he uploads a profile image
            "email": "user_email_address@domain_name.extension",
            "first_name": "user_firstname",
            "age": "user_age"
        }
    }
    ```

4. User login API:

    Request: POST `/user_app/login`

    Request Parameters:

    ```
    {
        "first_name":"user_firstname",
        "password":"user_password"
    }
    ```

    Response:

    ```
    {
        "status": "success",
        "data": {
            "last_name": "user_lastname",
            "id": user_unique_id,
            "profile": null,  ## user_profile_link_s3/default (null for now)
            "email": "user_email_address@domain_name.extension",
            "first_name": "user_firstname",
            "age": "user_age"
        }
    }
    ```

5. User API link to upload his/her profile picture (NOTE: All the profile pictures will be stored in S3 bucket)

    Request: PUT `/user_app/{id}/upload_image`

    Request Parameters: form_data with key as "image" and value as upload image.

    Response:

    ```
    {
        "status": "success",
        "data": {
            "last_name": "user_lastname",
            "id": user_unique_id,
            "profile": "s3://bucket_name/path_to_profile_dir/unique_uuid.jpg",  ## user_profile_link
            "email": "user_email_address@domain_name.extension",
            "first_name": "user_firstname",
            "age": "user_age"
        }
    }
    ```
