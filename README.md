# Flask backend API template

Template for backend API using the Flask framework, including user authentication and password reset by email

## API Reference
`http://example.com/api`

The API is organised around REST. The API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.

---
### Authentication
Most endpoints may be accessed only by an authenticated user.  Get a token from the `/tokens` endpoint using HTTP basic authentication (username and password).  This token is used to authenticate subsequent requests.  It expires after 60 minutes.

`POST /tokens`

#### Authentication
Basic

#### Example request
```
curl -X POST http://example.com/api/tokens \
-u {username}:{password}
```

#### Example response
```
{token}
```

Log out a user by revoking the authentication token.  This request must be authenticated using the token previously requested.

`DELETE /tokens`  
#### Authentication
Bearer token

#### Example request
```
curl -X DELETE http://example.com/api/tokens \
-H "Authorization: Bearer {token}"
```

#### Example response
```
None
```

---
### Users

Create a new user by making a request to the `/users` endpoint.  Pass JSON-encoded parameters in the request body.  The response includes a URI for retrieving the `user` object.

`POST /users`  

#### Request Body
`username` <sub>Required</sub>  
Username, must be unique.  

`email` <sub>Required</sub>  
Email address, must be unique.  

`password` <sub>Required</sub>  
Password

#### Authentication
None

#### Example request
```
curl http://example.com/api/users \
-d '{"username":"user", "email":"user@example.com", "password":"password"}' \
-H 'Content-Type: application/json'
```

#### Example response
```json
{
    "email": "user@example.com",
    "id":1,
    "uri": "/api/users/1",
    "username": "user"
}
```

Fetch information about user from the `users` endpoint, either specifying the user's username as a query parameter, or using the user's id to construct the URL.

`GET /users`  

#### Query Parameters
`u` <sub>Required</sub>  
Username.  

#### Authentication
Bearer token

#### Example request
```
curl 'http://example.com/api/users?u=user' \
-H 'Authorization: Bearer {token}'
```

#### Example response
```json
{
    "id": 1,
    "username": "user"
}
```

`GET /users/:id`  
#### Authentication
Bearer token

#### Example request
```
curl 'http://example.com/api/users/1' \
-H 'Authorization: Bearer {token}'
```

#### Example response
```json
{
    "id": 1,
    "username": "user"
}
```

---
### Passwords
Change or reset a user's password using the `passwords` endpoint.  Using this endpoint without authentication triggers a password reset email to the user's email address.  Authenticate with a valid token and a new password in the request body to change the user's password directly.

`PUT /passwords`  

#### Query Parameters
`u` <sub>Required</sub>  
Username.  

#### Request Body
`password` <sub>Optional</sub>  
New password.

#### Authentication
Bearer token (optional).  Use without authentication to request a password reset link by email.

#### Example request
Requesting a password reset link by email.
```
curl -X PUT 'http://example.com/api/passwords?u=user'
```

#### Example response
```
None
```

#### Example request
Changing a user's password.
```
curl -X PUT 'http://example.com/api/passwords?u=user' \
-H 'Authorization: Bearer {token}' \
-H 'Content-Type: application/json' \
-d '{"password": "new password"}'
```

#### Example response
```
None
```
