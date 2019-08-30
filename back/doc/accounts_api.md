#### **GET** */accounts/profile/*

Get the profile of the current user

Response:
```json
{
  "id": 1,
  "username": "jdoe",
  "first_name": "John",
  "last_name": "Doe",
  "email" : "jdoe@org.com",
  "photo": "S3 URL to profile photo",
  "roles": ["user", "admin"]
}
```

#### **PUT** */accounts/profile/*
Update the profile of the current user
> The roles can only be updated by an admin.

Request:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "jdoe@company.com"
}
```
> To update the profile photo use another API.

Response:
- status code: 200 OK

#### **POST** */accounts/photo/sign/*
Sign the URL for S3 storage of the current user profile photo.

Request:
```json
{
  "filename": "photo.jpg"
}
```
> The server will automatically add the folder of the photo.

Response: 
```json
{
  "filename": "photo.jpg",
  "url": "S3 signed URL"
}
```

#### **PUT** */accounts/photo/*
Update the profile with new photo filename.

Request:
```json
{
  "filename":"photo.jpg"
}
```

Response:
- status code: 200 OK

#### **POST** */accounts/password/*
Change password.

Request:
```json
{
  "password": "new password"
}
```

Response:
- status code: 200 OK
- status code: 400 Bad request. The new password is too weak.

### Admin APIs

*NOT IMPLEMENTED*

Same APIs as per user API but the base URL is `/accounts/admin/user/{}/`.

#### **POST** */accounts/admin/user/{}/password/*
Change password.
> API for admin only. Changing the password, it will update the field `reset_password` 
> forcing the user to reset his/her password upon the first login.

Permission required:
- is_superuser

Request:
```json
{
  "password": "new password"
}
```

Response:
- status code: 200 OK
- status code: 400 Bad request. The new password is too weak.
