
## Album 

#### **GET** */albums/*

Get all albums which the current user can view them

Permissions requested:
- view_album

Filters:
 - period: start, end
 
 > /albums/?start=01/01/2019&end=02/02/2019
 - category: category
 
 > /albums/?category=cat1&category=cat2
 - tag: tag
 
 >/albums/?tag=tag1&tag=tag2

 - favorites

> /albums/?favorites

Response:

- status code : 200 OK
```json
{
    "id": "id album",
    "name": "name album",
    "description": "descriere album",
    "date": "data album",
    "preview": "URL preview photo S3",
    "categories" : [ "categorie_1", "categorie_2" ],
    "tags" : ["tag 1", "tag 2"],
    "favorites": "true"
}
```

#### **GET** */albums/user/{user_id}*

Get all albums for which the owner is *user_id* and the 
current owner has the right to view them.

Response:

- status code : 200 OK
```json
{
    "id": "id album",
    "name": "name album",
    "description": "descriere album",
    "date": "data album",
    "preview": "URL preview photo S3",
    "categories" : [ "categorie_1", "categorie_2" ],
    "tags" : ["tag 1", "tag 2"],
    "favorites": "true"
}
```

#### **POST** */album/*
 
Create album
 
Permission required:
- create_album

Request:
 
```json
    {
      "name": "name album",
      "description": "descriere album",
      "date": "data album"
    }
```

Response:
- status code: 201 (CREATED)
- body: 
```json
{ 
  "id": "id-ul noului album" 
}
```

- status code: 403 FORBIDDEN if user has no right to create album 
	
#### **DELETE** */album/{id}*

Delete the album

Permissions requested:
- delete_album

Response:
- status code: 200 OK
- status code: 403 FORBIDDEN if the user has no delete permission
- status code: 404 album not found

#### **PUT** */album/{id}/*

Update album

Permissions requested:
- update_album

Request:

```json
{
    "name": "name album",
    "description": "descriere album",
    "date": "data album"
}
```
Response:
- status code: 200 (CREATED)
- status code: 403 FORBIDDEN 
  if user has no "delete" permission
- status code: 404 album not found

#### **GET** */album/{id}/permissions/*

Get the permissions of all users for album *id*.

> **The current user has to be the owner of the album.**

Response:
- status code: 200 OK
    - body
```json
[
  {
    "user_id": 1,
    "permissions": ["add_photo","view_photo"]
  }, 
  {
    "user_id": 2,
    "permissions": ["add_photo","view_photo"]
  }
]
```
- status code: 403 if current user is not the owner
- status code: 404 album not found

#### **POST** */album/{id}/permissions/*

Add new permissions to album *id* by the owner 

Response:
- status code: 200 OK
    - body
```json
[
  {
    "user_id": 1,
    "permissions": ["add_photo","view_photo"]
  }, 
  {
    "user_id": 2,
    "permissions": ["add_photo","view_photo"]
  }
]
```
- status code: 403 if current user is not the owner
- status code: 404 album not found

#### **DELETE** */album/{id}/permissions*

Remove permissions for album *id* 

Response:
- status code: 200 OK
    - body
```json
[
  {
    "user_id": 1,
    "permissions": ["add_photo","view_photo"]
  }, 
  {
    "user_id": 2,
    "permissions": ["add_photo","view_photo"]
  }
]
```
- status code: 403 if current user is not the owner
- status code: 404 album not found

#### **GET** */album/{id}/categories*

Get categories for album *id*

Permissions required:
- view_album

Response:
- status code: 200 OK
```json
    ["category1", "category2"]
```
- status code: 403 if no *view_album* permission
- status code: 404 album not found

#### **POST** */album/{id}/category*

Permission required:
- change_album

Request:
```json
["cateogry1", "category2"]
```

Response:
- status code: 200 OK
- status code: 403 if no *change_album* permission

#### **DELETE** */album/{id}/category/{name category}/*

Permission required:
- change_album

Response:
- status code: 200 OK
- status code: 403 if no *change_album* permission
- status code: 404 album not found

#### **PUT** */album/{id}/category/{name category}/*

Update *name category*

Request:
```json
    {"category": "new category"}
```

Response:
- status code: 200 OK
- status code: 403 if no *change_album* permission
- status code: 404 album not found

#### **GET** */album/{id}/tags*

Get tags for album *id*

Permissions required:
- view_album

Response:
- status code: 200 OK
```json
    ["tag 1", "tag 2"]
```
- status code: 403 if no *view_album* permission
- status code: 404 album not found

#### **POST** */album/{id}/tag*

Permission required:
- change_album

Request:
```json
["tag 1", "tag 2"]
```

Response:
- status code: 200 OK
- status code: 403 if no *change_album* permission

#### **DELETE** */album/{id}/tag/{name tag}/*

Permission required:
- change_album

Response:
- status code: 200 OK
- status code: 403 if no *change_album* permission
- status code: 404 album not found

#### **PUT** */album/{id}/tag/{name tag}/*

Update *name category*

Request:
```json
    {"tag": "new tag"}
```

Response:
- status code: 200 OK
- status code: 403 if no *change_album* permission
- status code: 404 album not found

#### **POST** */album/{id}/favorites/*

Set album as favorites for current user

Permission required:
- view_album

Response:
- status code: 200 OK
- status code: 403 if no *view_album* permission
- status code: 404 album not found

#### **DELETE** */album/{id}/favorites/*

Unset album as favorites for current user

Permission required:
- view_album

Response:
- status code: 200 OK
- status code: 403 if no *view_album* permission
- status code: 404 album not found

## Photo
 
#### **GET** */photo/album/{id}*
 
Get all photos from album *id*

Permissions requested:
- view_photo
- view_album

Response:
- status code = 200
- body:

```json
{
  "photos" : [{ 
                 "id": "id_poze",
                 "url": "s3 url"
              }],
  "thumbnails" : [{ 
                    "id": "id_poze",
                    "url": "s3 url"
                }]
}
```  
- status code = 403 FORBIDDEN daca nu are acces la album
- status code = 404 Not found


#### **POST** */photo/sign/*
 
Sign S3 url for upload

Permissions requested:
- add_photo

Request:

```json
{
  "album_id": "id-ul albumului",
  "filename": "numele pozei",
  "filetype": "tipul fisierului"
}
```
Response:

- status code=200
    - body:
```json
{
    "photo": "sign S3 url",
    "thumbnail": "sign S3 url pentru thumbnail"
}
```
            
            
- status code=403 daca utilizatorul nu are dreptul de a adauga poze
- status code=404 daca album nu exista

#### **POST** */photo/album/{id}*
 
Adauga poza in album (in prealabil poza a fost uploadata in S3)

Permissions requested:
- add_photo

Request:

```json
    {
        "album_id": "id-ul albumului",
        "filename": "filename",
        "thumbnail": "numele thumbnail"
    }
```

Response:
- status code = 200 OK
- status code = 403 if user has no *add_photo* permission
- status code=404 

#### **DELETE** */photo/{id}*
 
Delete the photo

Permissions requested:
- delete_photo

Response:
- status code = 200 OK
- status code = 403 FORBIDDEN
- status code = 404 Not found

### Summary


| Method | API                                   | Action                               |       Permission      | Owner | Comment |
|--------|---------------------------------------|--------------------------------------|:---------------------:|:-----:|---------|
| GET    | /albums/                              | Get albums                           |       view_album      |       |         |
| POST   | /album/                               | Create album                         |      create_album     |       |         |
| DELETE | /album/{id}                           | Delete album                         |      delete_album     |       |         |
| PUT    | /album/{id}                           | Update album *id*                    |      update_album     |       |         |
| GET    | /album/{id}/permissions/*             | Get users permissions for album *id* |          N/A          |  Yes  |         |
| POST   | /album/{id}/permissions/              | Add permissions                      |          N/A          |  Yes  |         |
| DELETE | /album/{id}/permissions               | Delete permissions                   |          N/A          |  Yes  |         |
| GET    | /album/{id}/categories                | Get categories for album *id*        |       view_album      |       |         |
| POST   | /album/{id}/category                  | Add category to album                | update_album          |       |         |
| DELETE | album/{id}/category/{name category}/  | Delete category from album           | update_album          |       |         |
| PUT    | /album/{id}/category/{name category}/ | Update *name category*               | update_album          |       |         |
| GET    | /album/{id}/tags                      | Get tags for album *id*              | view_album            |       |         |
| POST   | /album/{id}/tag                       | Add tag to album                     | update_album          |       |         |
| DELETE | /album/{id}/tag/{name_tag}            | Delete tag                           | update_album          |       |         |
| PUT    | /album/{id}/tag/{name tag}/           | Update *name tag*                    | update_album          |       |         |
| POST   | /album/{id}/favorites/                | Make album favorites for user        |                       |       |         |
| DELETE | /album/{id}/favorites/                | Remove album from favorites          |                       |       |         |
| GET    | /photo/album/{id}                     | Get photos for album *id*            | view_photo view_album |       |         |
| POST   | /photo/sign/                          | Generate presign S3 URL              | add_photo             |       |         |
| POST   | /photo/album/{id}                     | Add photo to album *id*              | add_photo             |       |         |
| DELETE | /photo/{id}                           | Delete photo *id*                    | delete_photo          |       |         |
