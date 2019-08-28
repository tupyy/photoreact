### Summary
| Method | API                                    | Action                                        |       Permission      | Owner | Comment |
|--------|----------------------------------------|-----------------------------------------------|:---------------------:|:-----:|---------|
| GET    | /favorites/album/{id}                  | Get users for which the album is favorites    |                       |  Only |         |
| GET    | /favorites/                            | Get all the favorites albums for current user |                       |       |         |
| POST   | /favorites/album/{id}/                 | Make album favorites for current user         |      view_permission  |       |         |
| DELETE | /favorites/album/{id}/                 | Remove album from favorites                   |                       |       |         |

#### **GET** */favorites/albumm/{id}/*
Get the list of users for which the album is favorites
> Only the owner of the album can access this API

Permission_required:
 - is_owner
 
Response:
```json
  {
    "album_id": 1,
    "users": ["user1", "user2"]
  }
```
- status code: 200 OK
- status code: 403 User is not the owner
- status code: 404 Album not found

#### **GET** */favorites/*
Get the list of favorites album for current user

Permission_required
- view_album

Response
```json
  {
    "albums": ["album1", "album2"]
  }
```
- status code: 200 OK

#### **POST** */favorites/album/{id}/*

Set album as favorites for current user

Permission required:
- view_album

Response:
- status code: 200 OK
- status code: 403 if no *view_album* permission
- status code: 404 album not found

#### **DELETE** */favorites/album/{id}/*

Unset album as favorites for current user

Response:
- status code: 200 OK
- status code: 400 Bad request if album is not favorite of user
- status code: 404 album not found
