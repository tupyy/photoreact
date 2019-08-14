
## Album 

#### **GET** */albums/*

Get all albums which the current user can view them

Permissions required:
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

#### **GET** */albums/owner/{user_id}*

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
      "date": "data album",
      "folder_path": "bucket/folder/"
    }
```

Response:
- status code: 201 (CREATED)
- body: 
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

- status code: 403 FORBIDDEN if user has no right to create album 
	
#### **DELETE** */album/{id}*

Delete the album

Permissions required:
- delete_album

Response:
- status code: 200 OK
- status code: 403 FORBIDDEN if the user has no delete permission
- status code: 404 album not found

#### **PUT** */album/{id}/*

Update album

Permissions required:
- update_album

Request:

```json
{
    "name": "name album",
    "description": "descriere album",
    "date": "data album",
    "folder_path": "bucket/folder/"
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
    [
      {
        "id": 1,
        "username": "batman",
        "permissions": [["Add photos", "add_photo"],["View photos, view_photo"]]
      }, 
      {
        "id": 2,
        "username": "superman",
        "permissions": [["Add photos", "add_photo"],["View photos, view_photo"]]
      }
    ],
    [
      {
        "id": 1,
        "group_name": "batman_friends",
        "permissions": [["Add photos", "add_photo"],["View photos, view_photo"]]
      }
    ]
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
["category1", "category2"]
```

Response:
- status code: 200 OK
- status code: 403 if no *change_album* permission

#### **DELETE** */album/{id}/category/{id category}/*

Permission required:
- change_album

Response:
- status code: 200 OK
- status code: 403 if no *change_album* permission
- status code: 404 album not found

#### **PUT** */album/{id}/category/{id category}/*

Update *id category*

Request:
```json
    {"category_id": 2}
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

#### **DELETE** */album/{id}/tag/{id tag}/*

Permission required:
- change_album

Response:
- status code: 200 OK
- status code: 403 if no *change_album* permission
- status code: 404 album not found

#### **PUT** */album/{id}/tag/{id tag}/*

Update *id tag*

Request:
```json
    {"tag_name": "new tag name"}
```
> Tag will be created if it do not exists

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
 
#### **GET** */photos/album/{id}/*
 
Get all photos from album *id*

Permissions required:
- view_photo
- view_album

Response:
- status code = 200
- body:

```json
  [
    { 
     "id": 1,
     "album_id": 2,
     "filename": "bar.jpg",
     "thumbnail_file": "thumbnail.jpg",
     "data": "2019/01/01",
     "get_photo_url": "s3 url",
     "get_thumbnail_url": "S3 GET url"
    }
  ]
```
> The photos inherits album permissions but the permission can be changed.
> Therefore, the user can view only the photos for which he has *view_photo* permission.  
- status code = 403 FORBIDDEN if user hs no *view_album* permission
- status code = 404 Not found


#### **POST** */photo/sign/album/{id}/*
 
Sign S3 url for upload to album *id*

Permissions required:
- add_photos

Request:

```json
{
  "filename": "numele pozei",
}
```
Response:

- status code=200
    - body:
```json
{
    "photo_url": "sign S3 url for put method",
    "thumbnail_filename": "123456.jpg",
    "thumbnail_url": "sign S3 url for put method"
}
```       
- status code=403 daca utilizatorul nu are dreptul de a adauga poze
- status code=404 daca album nu exista

#### **POST** */photo/album/{id}/*
 
Adauga poza in album (in prealabil poza a fost uploadata in S3)

Permissions required:
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

#### **DELETE** */photo/{id}/*
 
Delete the photo

Permissions required:
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
| DELETE | /album/{id}/                          | Delete album                         |      delete_album     |       |         |
| PUT    | /album/{id}/                          | Update album *id*                    |      update_album     |       |         |
| GET    | /album/{id}/permissions/*             | Get users permissions for album *id* |          N/A          |  Yes  |         |
| POST   | /album/{id}/permissions/              | Add permissions                      |          N/A          |  Yes  |         |
| DELETE | /album/{id}/permissions/              | Delete permissions                   |          N/A          |  Yes  |         |
| GET    | /album/{id}/categories/               | Get categories for album *id*        |       view_album      |       |         |
| POST   | /album/{id}/category/                 | Add category to album                | update_album          |       |         |
| DELETE | album/{id}/category/{id category}/    | Delete category from album           | update_album          |       |         |
| PUT    | /album/{id}/category/{id category}/   | Update *id category*                 | update_album          |       |         |
| GET    | /album/{id}/tags/                     | Get tags for album *id*              | view_album            |       |         |
| POST   | /album/{id}/tag/                      | Add tag to album                     | update_album          |       |         |
| DELETE | /album/{id}/tag/{id tag}/             | Delete tag                           | update_album          |       |         |
| PUT    | /album/{id}/tag/{id tag}/             | Update *id tag*                      | update_album          |       |         |
| POST   | /album/{id}/favorites/                | Make album favorites for user        |                       |       |         |
| DELETE | /album/{id}/favorites/                | Remove album from favorites          |                       |       |         |
| GET    | /photo/album/{id}                     | Get photos for album *id*            | view_photo view_album |       |         |
| POST   | /photo/sign/                          | Generate presign S3 URL              | add_photo             |       |         |
| POST   | /photo/album/{id}                     | Add photo to album *id*              | add_photo             |       |         |
| DELETE | /photo/{id}                           | Delete photo *id*                    | delete_photo          |       |         |
