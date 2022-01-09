# BODYX Service

## Authentication

Send a request with basic auth.

```json
{
    "username": "username",
    "password": "password"
}
```

To make any API request, include the token received from a successful login as the value of the key `x-access-token` in the header of the request.

```json
{
    "data": {
        "token": "sampleToken$eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.ey..."
    },
    "error": "",
    "message": "Login success"
}
```

## Usage

Headers should include `content-type` and`x-access-token`. All responses should have the form:

```json
{
	"data": "content of response",
	"msg": "message on success",
    "error": "message on error",
}
```

## Viewer and Admin API

## Admin only API

### List all shows

**Definition** `GET /shows`

**Response** `200 OK` on success

### Find a show

**Definition** `GET /shows/<id>`

**Response** `200 OK` on success

### Registering a new show

**Definition** `POST /shows`

**Arguments**

- `"enTitle":string`
- `"cnTitle":string`
- `"durationMins":integer`

**Response** 

- `201 Created` on success
- `400 Bad request` on invalid input

```json
{
	"id": "61d5ac4958b919489f458d9f",
	"enTitle": "English",
	"cnTitle": "中文",
	"durationMins": 120,
}
```

### Update a show

**Definition** `PUT /shows/<id>`

**Arguments**

- `"id":integer`
- `"enTitle":string`
- `"cnTitle":string`
- `"durationMins":integer`

**Response** 

- `201 Created` on success
- `404 Not found`
- `400 Bad request` on invalid input or id

### Delete a show

**Definition** `DELETE /shows/<id>`

**Response** 

- `204 No content` on success
- `404 Not found`
- `400 Bad request` on invalid id

### List all sessions

**Definition** `GET /sessions`

**Response** `200 OK` on success

### Find a session

**Definition** `GET /sessions/<id>`

**Response** `200 OK` on success

### Filter sessions by show id

**Definition** `GET /sessions?show_id=<id>`

**Response** `200 OK` on success

### Registering a new session

**Definition** `POST /shows`

**Arguments**

- `"dateTime":string` must be in ISO8601 format (see below)
- `"eventId":string`
- `"showId":string` must correspond to some show id

**Response** 

- `201 Created` on success
- `400 Bad request` on invalid input

```json
{
	"dateTime": "2012-01-01T23:30:00+02:00",
    "eventId": "first",
    "showId": "61d5ac4958b919489f458d9f",
}
```

### Update a session

**Definition** `PUT /shows/<id>`

**Arguments**

- `"dateTime":string`
- `"eventId":string`
- `"showId":string` 
- `"isPlaying":bool` 
- `"rooms":list`

**Response** 

- `201 Created` on success
- `404 Not found`
- `400 Bad request` on invalid input or id

```json
{
	"isPlaying": True,
	"rooms": [
		{
			"title": "Round Table",
            "url": "new_url",
            "isUnlocked": True,
		},
		{
			"title": "Cashier Counter",
            "url": "another_new_url",
            "isUnlocked": False,
		}
	]
}	
```



### Delete a session

**Definition** `DELETE /shows/<id>`

**Response** 

- `204 No content` on success
- `404 Not found`
- `400 Bad request` on invalid id