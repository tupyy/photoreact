## Activity log API

#### **GET** */activities/?start_date={date}&end_date={date}&page={number_of_page}*

Get activities log for current user filtered by period and ordered by date  
> Page size is set to 100 entries.

Response:
- 200 OK
```json
{
  "count": "number of log entries",
  "next": "next page url",
  "previous": "previous page url",
  "results": [
     {
       "content_object": "serialized data of the content object (Album or Photo)",
       "user": "user id",
       "date": "log date",
       "activity": "create"
     }  
   ]
}
```
- 403 User not logged 
