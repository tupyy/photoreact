
## Album 

**GET** */albums/*

>listeaza toate albumele pe care current_user poate sa le vizualizeze

Permissions requested:
- view_album

Filtre:
 - perioada: start, end
 - categorie: category
 - tag: tag

Response:

```json
{
    "id": "id album",
    "name": "name album",
    "description": "descriere album",
    "date": "data album",
    "preview": "URL preview photo S3",
    "categories" : [ "categorie_1", "categorie_2" ],
    "tags" : ["tag 1", "tag 2"] 
}
```

**POST** */album/*
 
> Create album
 
 Request:
  
```json
    {
      "name": "name album",
      "description": "descriere album",
      "date": "data album",
      "categories" : [ "categorie_1", "categorie_2" ],
      "tags" : ["tag 1", "tag 2"]
    }
```

Reponse:
- status_code: 201 (CREATED)
- body: 
```json
{ 
  "id": "id-ul noului album" 
}
```

- status_code: 403 FORBIDDEN if user has no right to create album 
	
**DELETE** */album/{id}*

> Delete the album

Permissions requested:
- delete_album

Response:
- status_code: 200 OK
- status_code: 403 FORBIDDEN if the user has no delete permission
- status_code: 404 Not found

**PUT** */album/*

Permissions requested:
- update_album

> Update album

Request:

```json
{
    "id": "id album",
    "name": "name album",
    "description": "descriere album",
    "date": "data album",
    "categories" : [ "categorie_1", "categorie_2" ],
    "tags" : ["tag 1", "tag 2"]
}
```
Response:
- status_code: 200 (CREATED)
- status_code: 403 FORBIDDEN 
  if user has no "delete" permission
- status_code: 404 Not found

**GET** */album/{id}/permissions/*

> Get the permissions of all users for album *id*.

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

**POST** */album/{id}/permissions/*

> Add new permissions to album *id* by the owner 

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

**DELETE** */album/{id}/permissions*

> Remove permissions for album *id* 
>

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

## Photo
 
> Api-uri pentru poze

**GET** */photo/album/{id}*
 
> Get all photos from album *id*

Permissions requested:
- view_album

Response:
- status_code = 200
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
- status_code = 403 FORBIDDEN daca nu are acces la album
- status_code = 404 Not found


**POST** */photo/sign/*
 
> Sign S3 url pentru poze

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

- status_code=200
    - body:
```json
{
    "photo": "sign S3 url",
    "thumbnail": "sign S3 url pentru thumbnail"
}
```
            
            
- status_code=403 daca utilizatorul nu are dreptul de a adauga poze
- status_code=404 daca album nu exista

**POST** */photo/*
 
> Adauga poza in album (in prealabil poza a fost uploadata in S3)

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
- status_code = 200 OK
- status_code = 403 if user has no *add_photo* permission
- status_code=404 

**DELETE** */photo/{id}*
 
> Sterge poza 

Permissions requested:
- delete_photo

Response:
- status_code = 200 OK
- status_code = 403 FORBIDDEN
- status_code = 404 Not found


 
