-- insert product categories
INSERT INTO product_category (name)
VALUES
  ('Shirts'),
  ('Pants'),
  ('Shoes'),
  ('Accessories');

-- insert products
INSERT INTO product (name, price, description, category_id, quantity)
VALUES
  ('T-Shirt', 19.99, 'A comfortable shirt.', 1, 0),
  ('Polo Shirt', 29.99, 'A shirt for looking fancy.', 1, 1),
  ('Jeans', 49.99, 'Pants for casual wear.', 2, 2),
  ('Khakis', 59.99, 'Pants for looking fancy.', 2, 3),
  ('Sneakers', 39.99, 'Shoes for casual wear.', 3, 4),
  ('Dress Shoes', 69.99, 'Shoes for looking fancy.', 3, 5),
  ('Watch', 299.99, 'A watch for looking fancy.', 4, 6),
  ('Necklace', 199.99, 'A necklace for looking fancy.', 4, 7);
