# Project Title

REST API using FastAPI

## Routes

### List Posts
```
GET: https://fastapi--wt-blog.herokuapp.com/posts
```
List posts containing entered characters Limit : Max # of posts to return Offset: Skip X number of entries

#### Parameters

Limit (integer) : Default Value 10
Offset (integer): Defualt Value 0
Search (string) : Default Value ""

Successful Response 200 OK:

```JSON
[
  {
    "Post": {
      "title": "string",
      "content": "string",
      "published": true,
      "owner_id": 0,
      "post_id": 0,
      "created_at": "2023-02-02T13:49:06.844Z",
      "owner": {
        "id": 0,
        "email": "user@example.com"
      }
    },
    "votes": 0
  }
]
```
Invalid Authentication 401 Unauthorized:

```JSON
{
    "detail": "Not authenticated"
}
```

## Description

Full Documentation:
https://fastapi--wt-blog.herokuapp.com/docs

### Dependencies

```
alembic==1.9.1
anyio==3.6.2
autopep8==2.0.1
bcrypt==4.0.1
cffi==1.15.1
click==8.1.3
cryptography==39.0.0
dnspython==2.2.1
ecdsa==0.18.0
email-validator==1.3.0
fastapi==0.88.0
h11==0.14.0
httptools==0.5.0
idna==3.4
Mako==1.2.4
MarkupSafe==2.1.1
passlib==1.7.4
psycopg2==2.9.5
pyasn1==0.4.8
pycodestyle==2.10.0
pycparser==2.21
pydantic==1.10.4
python-dotenv==0.21.0
python-jose==3.3.0
python-multipart==0.0.5
PyYAML==6.0
rsa==4.9
six==1.16.0
sniffio==1.3.0
SQLAlchemy==1.4.46
starlette==0.22.0
tomli==2.0.1
typing_extensions==4.4.0
uvicorn==0.20.0
uvloop==0.17.0
watchfiles==0.18.1
websockets==10.4

```

## Limitations

The current iteration of the API does not support User First Name and Last Name integration within the database, this version only supports email and id identification. Future versions will support
First Name and Last Name for each User that is generated.

## Author Information

Name: Wali Temuri9
Contact: walitemuri@gmail.com

## Development History
