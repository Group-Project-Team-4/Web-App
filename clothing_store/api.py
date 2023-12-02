from flask import Blueprint, jsonify, request
from clothing_store.db import get_db

bp = Blueprint('api', __name__)


@bp.route('/api/products', methods=['GET'])
def get_products():
    db = get_db()
    products = db.execute('SELECT id, name, price, description, quantity, category_id FROM product')

    response = {"success": True, "products": []}
    for item in products:
        response["products"].append(dict(item))

    return jsonify(response)


# There was no endpoint planned in the overview for retrieving a single product,
# but I think having one will be useful and important for testing.
@bp.route('/api/products/<int:id>', methods=['GET'])
def get_product(id: int):
    db = get_db()

    product = db.execute('SELECT id, name, price, description, quantity, category_id FROM product WHERE id = ?', str(id))
    if not product:
        return jsonify({'error': f'Item with ID {id} not found.'})

    return {"success": True, "product": dict(product.fetchone())}


@bp.route('/api/products', methods=['POST'])
def add_product():
    db = get_db()
    product = request.json['product']
    if validate_product(product):
        # Organize data for inserting into the database.
        data = (product['name'],
                product['price'],
                product['description'],
                product['quantity'],
                product['category_id'])

        # Insert the new product and commit the change to the database
        db.execute('INSERT INTO product (name, price, description, quantity, category_id) VALUES(?, ?, ?, ?, ?)', data)
        db.commit()
        # Retrieve newly added product to include in the response using the name and description
        db_product = dict(db.execute('SELECT id, name, price, description, quantity, category_id FROM product WHERE name = ? AND description = ?', (product['name'], product['description'])).fetchone())
        response = {"success": True, "product": db_product}
        return response, 201
    else:
        return jsonify({'error': 'Invalid product information.'})


def validate_product(product: dict):
    # Check every value to ensure it is both present and valid.
    if not isinstance(product['quantity'], int) or product['quantity'] < 0:
        return False
    if not isinstance(product['category_id'], int) or product['category_id'] < 0:
        return False
    if not isinstance(product['price'], float) or product['price'] < 0:
        return False
    if not isinstance(product['name'], str):
        return False
    if not isinstance(product['description'], str):
        return False

    return True


@bp.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id: int):
    db = get_db()

    # Error if the given ID does not exist in the database yet.
    product_exists = db.execute('SELECT id FROM product WHERE id = ?', (id))
    if not product_exists:
        return jsonify({'error': f'Product with ID {id} not found.'})

    new_data = request.json['product']
    # Iterate through every key/value included in the request
    for key, value in new_data.items():
        if not validate_new_data((key, value)):
            return jsonify({'error': 'Invalid product information.'})
        else:
            # To avoid SQL injection-prone code, and to use SQLite parameterization appropriately,
            # the key is matched to a specific SQL statement. Errors out if not found.
            match key:
                case 'name':
                    db.execute('UPDATE product SET name = ? WHERE id = ?', (value, id))
                case 'description':
                    db.execute('UPDATE product SET description = ? WHERE id = ?', (value, id))
                case 'quantity':
                    db.execute('UPDATE product SET quantity = ? WHERE id = ?', (value, id))
                case 'category_id':
                    db.execute('UPDATE product SET category_id = ? WHERE id = ?', (value, id))
                case 'price':
                    db.execute('UPDATE product SET price  = ? WHERE id = ?', (value, id))
                case _:
                    return jsonify({'error': 'Invalid product information.'})

            db.commit()

    # Product with new data is retrieved from the database for response
    db_product = dict(db.execute('SELECT id, name, price, description, quantity, category_id FROM product WHERE id = ?', str(id)).fetchone())
    response = {"success": True, "product": db_product}
    return response


def validate_new_data(data: tuple):
    key = data[0]
    value = data[1]
    match key:
        case 'quantity' | 'category_id':
            if not isinstance(value, int) or value < 0:
                return False
        case 'price':
            if not isinstance(value, float) or value < 0:
                return False
        case 'name' | 'description':
            if not isinstance(value, str):
                return False

    return True


@bp.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id: int):
    db = get_db()

    # Error if the given ID does not exist in the database.
    product_exists = db.execute('SELECT id FROM product WHERE id = ?', (id))
    if not product_exists:
        return jsonify({'error': f'Product with ID {id} not found.'})

    db.execute('DELETE FROM product WHERE id = ?', (id))
    db.commit()

    return jsonify({'success': True})
