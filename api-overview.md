## API Overview

API for clothing store products under the `/api/products` route. Each method responds with data in a JSON format and some methods require a request with a specific JSON format. Example requests and responses for each method can be seen below.

---

### `GET` `/api/products`

Returns all products in the database

#### Request
No JSON is needed for this request.

#### Response
```json
{
    "success": true,
    "products": [
        {
            "id": 1,
            "name": "T-Shirt",
            "price": 19.99,
            "description": "A comfortable shirt.",
            "quantity": 0,
            "category_id": 1,
        }
        {
            "id": 2,
            "name": "Polo Shirt",
            "price": 29.99,
            "description": "A shirt for looking fancy.",
            "quantity": 1,
            "category_id": 1,
        }
        ...
    ]
}
```

---

### `POST` `/api/products`

Adds a product to the database.

#### Request

```json
{
    "product": {
        "name": "Running Shoes",
        "price": 49.99,
        "description": "Comfortable running shoes.",
        "quantity": 10,
        "category_id": 3,
    }
}

```

#### Response

```json
{
    "success": true,
    "product": {
        "id": 9,
        "name": "Running Shoes",
        "price": 49.99,
        "description": "Comfortable running shoes.",
        "quantity": 10,
        "category_id": 3,
    }
}
```

---

### `PUT` `/api/products/<id>`

Updates a product with an ID of `<id>`.

#### Request to `/api/products/1`

```json
{
    "product": {
        "price": 15.99
    }
}
```

#### Response

```json
{
    "success": true,
    "product": {
        "id": 1,
        "name": "T-Shirt",
        "price": 15.99, // updated price
        "description": "A comfortable shirt.",
        "quantity": 0,
        "category_id": 1,
    }
}
```

--- 

### `DELETE` `/api/products/<id>`

Deletes a product with an ID of `<id>`.

#### Request to `/api/products/1`
No request data is needed.

#### Response
```json
{
    "success": true
}
```
