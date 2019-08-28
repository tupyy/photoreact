| Method | API                                   | Action                               |       Permission      | Owner | Comment |
|--------|---------------------------------------|--------------------------------------|:---------------------:|:-----:|---------|
| GET    | /permissions/album/{id}/              | Get users permissions for album *id* |          N/A          |  Yes  |         |
| POST   | /permissions/album/{id}/              | Add permissions                      |          N/A          |  Yes  |         |
| DELETE | /permissions/album/{id}/              | Delete permissions                   |          N/A          |  Yes  |         |

#### **GET** */permissions/album/{id}/*

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

#### **POST** */permissions/album/{id}/*

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

#### **DELETE** */permissions/album/{id}/*

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
