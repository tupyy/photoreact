## Activity log API

#### **GET** */activities/*

Get activities log for current user filtered by period and ordered by date  
> Page size is set to 100 entries.

Query parameters:
- activity_from
- activity_to
- limit
- activity
- sortByAsc
- sortByDesc

Example:
* /activities?activity_from=2019-01-01&activity_to=2019-30-01&activity=c&sortByDesc=date*


Response:
- 200 OK
```json
{
  "count": "number of log entries",
  "next": "next page url",
  "previous": "previous page url",
  "results": [
     {
       "object_id": "id of the content object (Album or Photo)",
       "user": "user id",
       "date": "log date",
       "activity": "create"
     }  
   ]
}
```
- 403 User not logged 

#### **GET** */activities/user/{user_id}/*

Same API as before but allowed only for superuser. This API return the 
activity for user `user_id`

