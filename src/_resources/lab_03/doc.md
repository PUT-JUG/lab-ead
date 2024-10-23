### RESTful API Documentation

#### Base URL
```
http://localhost:5000
```

#### Authentication
All endpoints require a valid token to be included in the request headers.

- **Header:** `Authorization: Bearer <token>`

#### Endpoints

1. **Get all books**

   - **URL:** `/books`
   - **Method:** `GET`
   - **Description:** Retrieves a list of all books.
   - **Headers:**
     - `Authorization: Bearer <token>`
   - **Response Codes:**
     - `200 OK`: Successfully retrieved the list of books.
     - `401 Unauthorized`: Invalid or missing token.
   - **Example Call:**
     ```bash
     curl -X GET http://localhost:5000/books -H "Authorization: Bearer <token>"
     ```

2. **Get a book by ID**

   - **URL:** `/books/<id>`
   - **Method:** `GET`
   - **Description:** Retrieves a book by its ID.
   - **Headers:**
     - `Authorization: Bearer <token>`
   - **Response Codes:**
     - `200 OK`: Successfully retrieved the book.
     - `404 Not Found`: Book with the specified ID does not exist.
     - `401 Unauthorized`: Invalid or missing token.
   - **Example Call:**
     ```bash
     curl -X GET http://localhost:5000/books/1 -H "Authorization: Bearer <token>"
     ```

3. **Add a new book**

   - **URL:** `/books`
   - **Method:** `POST`
   - **Description:** Adds a new book to the collection.
   - **Headers:**
     - `Authorization: Bearer <token>`
   - **Request Body:**
     ```json
     {
       "title": "New Book Title",
       "author": "Author Name",
       "year": 2023
     }
     ```
   - **Response Codes:**
     - `201 Created`: Successfully added the new book.
     - `400 Bad Request`: The request body is invalid.
     - `401 Unauthorized`: Invalid or missing token.
   - **Example Call:**
     ```bash
     curl -X POST http://localhost:5000/books -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"title": "New Book Title", "author": "Author Name", "year": 2023}'
     ```

4. **Update a book by ID**

   - **URL:** `/books/<id>`
   - **Method:** `PUT`
   - **Description:** Updates the details of a book by its ID.
   - **Headers:**
     - `Authorization: Bearer <token>`
   - **Request Body:**
     ```json
     {
       "title": "Updated Book Title",
       "author": "Updated Author Name",
       "year": 2023
     }
     ```
   - **Response Codes:**
     - `200 OK`: Successfully updated the book.
     - `400 Bad Request`: The request body is invalid.
     - `404 Not Found`: Book with the specified ID does not exist.
     - `401 Unauthorized`: Invalid or missing token.
   - **Example Call:**
     ```bash
     curl -X PUT http://localhost:5000/books/1 -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"title": "Updated Book Title", "author": "Updated Author Name", "year": 2023}'
     ```

5. **Delete a book by ID**

   - **URL:** `/books/<id>`
   - **Method:** `DELETE`
   - **Description:** Deletes a book by its ID.
   - **Headers:**
     - `Authorization: Bearer <token>`
   - **Response Codes:**
     - `204 No Content`: Successfully deleted the book.
     - `404 Not Found`: Book with the specified ID does not exist.
     - `401 Unauthorized`: Invalid or missing token.
   - **Example Call:**
     ```bash
     curl -X DELETE http://localhost:5000/books/1 -H "Authorization: Bearer <token>"
     ```

### Explanation of Returned Codes

- **200 OK:** The request was successful, and the server returned the requested data.
- **201 Created:** The request was successful, and a new resource was created.
- **204 No Content:** The request was successful, but there is no content to send in the response.
- **400 Bad Request:** The server could not understand the request due to invalid syntax.
- **401 Unauthorized:** The request requires user authentication.
- **404 Not Found:** The server could not find the requested resource.

This documentation provides a clear overview of the available endpoints, their purposes, and example calls to interact with the API, including the necessary authentication tokens.