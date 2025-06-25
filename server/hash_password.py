import bcrypt

password = "admin123"  
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(hashed.decode())

# password = "emp123"  
# hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
# print(hashed.decode())

# password = "emp456"  
# hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
# print(hashed.decode())
