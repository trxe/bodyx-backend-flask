# BODYX Service

## Usage

All responses should have the form 

```json
{
	"data": "content of response",
	"message": "description"
}
```

### List all shows

**Definition** `GET /shows`

**Response** `200 OK` on success

```json
[
    {
        "id": 1,
        "enTitle": "",
        "cnTitle": "",
        "durationMins": 120,
    }
]
```

### Registering a new show

**Definition** `POST /shows`

**Arguments**

- `"enTitle":string`
- `"cnTitle":string`
- `"durationMins":integer`

**Response** 

- `201 Created` on success
- `405 Method not allowed` if identical `enTitle` and `cnTitle`

```json
{
	"id": 1,
	"enTitle": "",
	"cnTitle": "",
	"durationMins": 120,
}
```

### Update a show

**Definition** `PUT /shows/<identifier>`

**Arguments**

- `"id":integer`
- `"enTitle":string`
- `"cnTitle":string`
- `"durationMins":integer`

**Response** 

- `201 Created` on success
- `404 Not found`

```json
{
	"id": 1,
	"enTitle": "",
	"cnTitle": "",
	"durationMins": 120,
}
```

### Delete a show

**Definition** `DELETE /shows/1`

**Response** 

- `204 No content` on success
- `404 Not found`

```json
{
	"id": 1,
	"enTitle": "",
	"cnTitle": "",
	"durationMins": 120,
}
```

### 