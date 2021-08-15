import os, sys

sys.path.append('../lib')

import db_function as dbf
 
list_x= [2, 11.885]
list_y_db= [6, 21.5]
dBref = 1;#2e-5

for y_db in list_y_db:
    #y_db = dbf.db(x, dBref)
    y_lin = dbf.idb(y_db, dBref)
    """
    6.0 dB; line:1.995
    21.5 dB; line:11.885
    """    
    print("{:.1f} dB; line:{:.3f} ".format(y_db, y_lin) )