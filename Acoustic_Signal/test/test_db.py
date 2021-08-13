import db_function as dbf
 
x = 2
dBref = 2e-5
y_db = dbf.db(x, dBref)
y_lin = dbf.idb(y_db, dBref)
 
print(y_db)
print(y_lin)