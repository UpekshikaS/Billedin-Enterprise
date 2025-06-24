-- USERS
INSERT INTO users (email, password, full_name, role, subscription_active)
VALUES 
  ('admin@billedin.com', 'hashed_password_1', 'Admin User', 'admin', TRUE),
  ('employee1@billedin.com', 'hashed_password_2', 'Nanduni Upekshika', 'employee', TRUE),
  ('employee2@billedin.com', 'hashed_password_3', 'Ravindu Silva', 'employee', FALSE);

-- PRODUCTS
INSERT INTO products (name, price, stock)
VALUES 
  ('T-Shirt', 1200.00, 50),
  ('Jeans', 2500.00, 30),
  ('Dress', 3200.00, 20),
  ('Jacket', 4500.00, 10),
  ('Skirt', 1800.00, 25);

-- INVOICES
INSERT INTO invoices (user_id, total_amount)
VALUES 
  (2, 4900.00),
  (2, 2500.00),
  (3, 4500.00);

-- INVOICE ITEMS
INSERT INTO invoice_items (invoice_id, product_id, quantity, price)
VALUES 
  (1, 1, 2, 1200.00),
  (1, 2, 1, 2500.00),
  (2, 2, 1, 2500.00),
  (3, 4, 1, 4500.00);