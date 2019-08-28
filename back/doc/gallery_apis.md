
### Summary
| Method | API                                   | Action                               |       Permission      | Owner | Comment |
|--------|---------------------------------------|--------------------------------------|:---------------------:|:-----:|---------|
| GET    | /albums/                              | Get albums                           |       view_album      |       |         |
| GET    | /album/{id}/                          | Get album                            |       view_album      |       |         |
| POST   | /album/                               | Create album                         |      create_album     |       |         |
| DELETE | /album/{id}/                          | Delete album                         |      delete_album     |       |         |
| PUT    | /album/{id}/                          | Update album *id*                    |      update_album     |       |         |
| GET    | /album/{id}/categories/               | Get categories for album *id*        |       view_album      |       |         |
| POST   | /album/{id}/category/                 | Add category to album                | update_album          |       |         |
| DELETE | album/{id}/category/{id category}/    | Delete category from album           | update_album          |       |         |
| PUT    | /album/{id}/category/{id category}/   | Update *id category*                 | update_album          |       |         |
| GET    | /album/{id}/tags/                     | Get tags for album *id*              | view_album            |       |         |
| POST   | /album/{id}/tag/                      | Add tag to album                     | update_album          |       |         |
| DELETE | /album/{id}/tag/{id tag}/             | Delete tag                           | update_album          |       |         |
| PUT    | /album/{id}/tag/{id tag}/             | Update *id tag*                      | update_album          |       |         |
| GET    | /photos/album/{id}/                   | Get photos for album *id*            | view_photo view_album |       |         |
| POST   | /photo/sign/album/{id}                | Generate presign S2 URL              | add_photos            |       |         |
| POST   | /photo/album/{id}/                    | Add photo to album *id*              | add_photos            |       |         |
| DELETE | /photo/{id}/                          | Delete photo *id*                    | delete_photos         |       |         |
## Album 

#### **GET** */albums/*

Get all albums which the current user can view them

Permissions required:
- view_album

Filters:
 - period: album_from, album_to 
 - limit
 
 Ordering:
 - classic Django ordering query parameter
 
 Example:
 
*/albums/?album_from=01/01/2019&album_to=02/02/2019&limit=2*

Response:

- status code : 200 OK
```json
{
    "size": 1,
    "albums": [
      {
        "id": "1",
        "name": "name album",
        "description": "descriere album",
        "date": "data album",
        "preview": "URL preview photo S3",
        "categories" : [ "categorie_1", "categorie_2" ],
        "tags" : ["tag 1", "tag 2"]
      }
    ]
}
```

#### **GET** */albums/owner/{user_id}*

Get all albums for which the owner is *user_id* and the 
current owner has the right to view them.

Response:

- status code : 200 OK
```json
{
    "size": 1,
    "albums": [
      {
        "id": "1",
        "name": "name album",
        "description": "descriere album",
        "date": "data album",
        "preview": "URL preview photo S3",
        "categories" : [ "categorie_1", "categorie_2" ],
        "tags" : ["tag 1", "tag 2"],
      }
    ]
}
```

#### **GET** */album/{id}*
Get album

Permission required:
- view_album

Response:

```json
{
    "id": 1,
    "name": "name album",
    "description": "descriere album",
    "date": "data album",
    "preview": "URL preview photo S3",
    "categories" : [ "categorie_1", "categorie_2" ],
    "tags" : ["tag 1", "tag 2"]
}
```

- status code : 200 OK
- status code: 403 No `view_permission`
- status code: 404 Album not found

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
    "date": "data album"
}
```

- status code: 403 FORBIDDEN if user has no right to create album 
	
#### **DELETE** */album/{id}*

Delete the album

Permissions required:
- delete_album

Response:
- status code: 204 NO CONTENT 
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
```json
{
  "id": "1",
  "name": "name album",
  "description": "descriere album",
  "date": "data album",
  "preview": "URL preview photo S3",
  "categories" : [ "categorie_1", "categorie_2" ],
  "tags" : ["tag 1", "tag 2"],
  "favorites": "true"
}
```
- status code: 200 OK 
- status code: 403 FORBIDDEN 
  if user has no "delete" permission
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


## Photo
 
#### **GET** */photos/album/{id}/*
 
Get all photos from album *id*

Permissions required:
- view_photo
> This permission is on Photo model
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
- add_photos

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
- delete_photos

Response:
- status code = 200 OK
- status code = 403 FORBIDDEN
- status code = 404 Not found



