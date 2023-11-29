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


@bp.route('/api/products', methods=['POST'])
def add_product():
    db = get_db()
    product = request.json['product']
    if validate_product(product):
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
        return response
    else:
        return jsonify({'error': 'Invalid product information.'})


def validate_product(product: dict):
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

# TODO: Finish implementation of these endpoints
# @bp.route('/api/products/<int:id>', methods=['PUT'])
# def update_product(id: int):
#     db = get_db()
#     new_data = request.json['product']
#     if validate_new_data(new_data):
#    else:
#        return jsonify({'error': 'Invalid product information.'})


# def validate_new_data(data: dict):
#    for key, value in data:
#        match key:
#            case 'quantity' | 'category_id':
#                if not isinstance(value, int) or value < 0:
#                    return False
#            case 'price':
#                if not isinstance(value, float) or value < 0:
#                    return False
#            case 'name' | 'description':
#                if not isinstance(value, str):
#                    return False
#
#    return True

#@bp.route('/api/products/<int:id>', methods=('DELETE'))
#def delete_product(id: int):
