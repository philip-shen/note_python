# 2020/03/08 Initial
#################################################
import os,sys,logging,time
import csv,re

import json, yaml
import sqlite3
from sqlite3 import Error

from logger import logger

# 2020/06/25 Initial to sqlite test code
sql_create_table_3Quest_pub = """ CREATE TABLE IF NOT EXISTS _3Quest_pub (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    noise text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """
sql_create_table_3Quest_road = """ CREATE TABLE IF NOT EXISTS _3Quest_road (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    noise text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """
sql_create_table_3Quest_crossroad = """ CREATE TABLE IF NOT EXISTS _3Quest_crossroad (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    noise text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """
sql_create_table_3Quest_train = """ CREATE TABLE IF NOT EXISTS _3Quest_train (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    noise text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """
sql_create_table_3Quest_car = """ CREATE TABLE IF NOT EXISTS _3Quest_car (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    noise text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """                     
sql_create_table_3Quest_cafeteria = """ CREATE TABLE IF NOT EXISTS _3Quest_cafeteria (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    noise text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """                     
sql_create_table_3Quest_mensa = """ CREATE TABLE IF NOT EXISTS _3Quest_mensa (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    noise text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """                                            
sql_create_table_3Quest_callcenter = """ CREATE TABLE IF NOT EXISTS _3Quest_callcenter (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    noise text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """                                           
sql_create_table_3Quest_voice_distractor = """ CREATE TABLE IF NOT EXISTS _3Quest_voice_distractor (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    noise text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """                                               
sql_create_table_3Quest_nobgn = """ CREATE TABLE IF NOT EXISTS _3Quest_nobgn (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    noise text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """                                     
sql_create_table_3Quest_AVG = """ CREATE TABLE IF NOT EXISTS _3Quest_AVG (
                                                                    id integer PRIMARY KEY,
                                                                    SMOS text,
                                                                    NMOS text,
                                                                    GMOS text,
                                                                    delta_SNR text,
                                                                    noise text,
                                                                    dut_foldername text NOT NULL,
                                                                    insert_date text,
                                                                    insert_time text   
                                            ); """
sql_create_table_3Quest_path = """ CREATE TABLE IF NOT EXISTS _3Quest_path (
                                                                    id integer PRIMARY KEY,
                                                                    path text
                                            ); """                                            
sql_create_table_noise_type = """ CREATE TABLE IF NOT EXISTS noise_type (
                                                                    id integer PRIMARY KEY,
                                                                    name text,
                                                                    description text,
                                                                    path text
                                            ); """

sql_query_WiFi_DHCP_Avg = """ SELECT DISTINCT char_log.test_method, char_log.model, char_log.fw, 
                                char_csv.csv_foldername, char_csv.csv_filename, char_csv.throughput_avg
                                FROM Chariot_CSV_Throughput char_csv 
                                INNER JOIN Chariot_Log char_log ON char_csv.csv_foldername = char_log.csv_foldername  
                                WHERE char_csv.csv_filename REGEXP  '^Client[0-9]' and  char_log.test_method REGEXP  '^DHCP'
                                ORDER BY char_csv.csv_foldername ASC
                            ; """
sql_insert_table_3Quest_pub = ''' INSERT INTO _3Quest_pub(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        noise,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_road = ''' INSERT INTO _3Quest_road(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        noise,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_crossroad = ''' INSERT INTO _3Quest_crossroad(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        noise,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_train = ''' INSERT INTO _3Quest_train(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        noise,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_car = ''' INSERT INTO _3Quest_car(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        noise,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_cafeteria = ''' INSERT INTO _3Quest_cafeteria(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        noise,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_mensa = ''' INSERT INTO _3Quest_mensa(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        noise,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_callcenter = ''' INSERT INTO _3Quest_callcenter(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        noise,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_voice_distractor = ''' INSERT INTO _3Quest_voice_distractor(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        noise,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_nobgn = ''' INSERT INTO _3Quest_nobgn(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        noise,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_AVG = ''' INSERT INTO _3Quest_AVG(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        noise,
                                        dut_foldername,
                                        insert_date,
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_path = ''' INSERT INTO _3Quest_path(
                                        path)
                    VALUES(?) '''
sql_insert_table_noise_type = ''' INSERT INTO noise_type(
                                        name,
                                        description,
                                        path)
                    VALUES(?,?,?) '''
sql_query_table_noise_type_count = """  SELECT COUNT(*) FROM noise_type;
                             """

class DB_sqlite:
    def __init__(self, path_db_file, dut_foldername, insert_date, insert_time, path_dut, opt_verbose='OFF'):
        self.path_db_file = path_db_file
        self.dut_foldername = dut_foldername
        self.insert_date = insert_date
        self.insert_time = insert_time
        self.path_dut = path_dut
        self.opt_verbose = opt_verbose
        self.list_noise_file = [['000','nobgn',''], \
                          ['001', 'pub', ''], \
                          ['002', 'road', ''], \
                          ['003', 'crossroad', ''], \
                          ['004', 'train', ''], \
                          ['005', 'car', ''], \
                          ['006', 'cafeteria', ''], \
                          ['007', 'mensa', ''], \
                          ['008', 'callcenter', ''], \
                          ['009', 'voice_distractor', ''], \
                          ['010', 'AVG', ''] ]                                

    def create_connection(self):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(self.path_db_file)
            #print(sqlite3.version)
            return conn
        except Error as e:
            msg = "Error create_connection:{}"
            logger.info(msg.format(e))
            #print(e)
        
        return None

    def create_table(self,conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            msg = "Error create_table:{}"
            logger.info(msg.format(e))
            #print(e)

    #modulation,
    #,?    
    
    def create_all_tables_3Quest(self,conn):
        self.create_table(conn, sql_create_table_3Quest_pub)
        self.create_table(conn, sql_create_table_3Quest_road)
        self.create_table(conn, sql_create_table_3Quest_crossroad)
        self.create_table(conn, sql_create_table_3Quest_train)
        self.create_table(conn, sql_create_table_3Quest_car)
        self.create_table(conn, sql_create_table_3Quest_cafeteria)
        self.create_table(conn, sql_create_table_3Quest_mensa)
        self.create_table(conn, sql_create_table_3Quest_callcenter)
        self.create_table(conn, sql_create_table_3Quest_voice_distractor)
        self.create_table(conn, sql_create_table_3Quest_nobgn)
        self.create_table(conn, sql_create_table_3Quest_AVG)
        self.create_table(conn, sql_create_table_3Quest_path)

        self.create_table(conn, sql_create_table_noise_type)

    '''
    
    '''
    def create_csv3quest_many(self, conn, list_3quest_values):
        
        if self.opt_verbose.lower() == "on":
            msg = "self.insert_sql:{}"
            logger.info(msg.format(self.insert_sql))
            msg = "len(list_3quest_values): {}"
            logger.info(msg.format(len(list_3quest_values) ))

        try:
            cur = conn.cursor()
            # How to insert a list of lists into a table? [Python]
            #https://stackoverflow.com/questions/51503490/how-to-insert-a-list-of-lists-into-a-table-python

            # How do I use prepared statements for inserting MULTIPLE records in SQlite using Python / Django?
            # To use parameterized queries, and to provide more than one set of parameters
            #https://stackoverflow.com/questions/5616895/how-do-i-use-prepared-statements-for-inserting-multiple-records-in-sqlite-using
            list_tuple_csv3quest_s = [tuple(l) for l in list_3quest_values]
            #print(list_tuple_tseotcdailyinfo_s)
            cur.executemany(self.insert_sql, list_tuple_csv3quest_s)

        except sqlite3.Error as err:
            #print("Error occurred: %s" % err)
            msg = "Error occurred: {}"
            logger.info(msg.format(err))     
        else:
            #print('Total {} record(s) to insert table.'.format(cur.rowcount))
            msg = 'Total {} record(s) to insert table.'
            logger.info(msg.format(cur.rowcount))
        return cur.lastrowid

    # select noise name for sorting ex. no_bgn is first
    def select_noise_name(self,noise):
        noise_name=''

        for list_noise_name_desc in self.list_noise_file:
            noise_name=list_noise_name_desc[0]
            noise_desc=list_noise_name_desc[1]
            
            if noise in noise_desc: 
                if self.opt_verbose.lower() == "on":
                    msg = "noise:{}; noise_desc:{}"
                    logger.info(msg.format(noise, noise_desc))
                
                return noise_name

    def select_insert_tab_sql(self,noise):
        if re.search(r'pub', noise): 
            self.insert_sql=sql_insert_table_3Quest_pub 
            self.noise = self.select_noise_name(noise)

        if re.search(r'road', noise): 
            self.insert_sql=sql_insert_table_3Quest_road
            self.noise = self.select_noise_name(noise)

        if re.search(r'crossroad', noise): 
            self.insert_sql=sql_insert_table_3Quest_crossroad
            self.noise = self.select_noise_name(noise)

        if re.search(r'train', noise): 
            self.insert_sql=sql_insert_table_3Quest_train
            self.noise = self.select_noise_name(noise)

        if re.search(r'car', noise): 
            self.insert_sql=sql_insert_table_3Quest_car
            self.noise = self.select_noise_name(noise)

        if re.search(r'cafeteria', noise): 
            self.insert_sql=sql_insert_table_3Quest_cafeteria
            self.noise = self.select_noise_name(noise)

        if re.search(r'mensa', noise): 
            self.insert_sql=sql_insert_table_3Quest_mensa
            self.noise = self.select_noise_name(noise)

        if re.search(r'callcenter', noise): 
            self.insert_sql=sql_insert_table_3Quest_callcenter
            self.noise = self.select_noise_name(noise)

        if re.search(r'voice_distractor', noise): 
            self.insert_sql=sql_insert_table_3Quest_voice_distractor
            self.noise = self.select_noise_name(noise)

        if re.search(r'nobgn', noise): 
            self.insert_sql=sql_insert_table_3Quest_nobgn
            self.noise = self.select_noise_name(noise)

        if re.search(r'AVG', noise): 
            self.insert_sql=sql_insert_table_3Quest_AVG
            self.noise = self.select_noise_name(noise)

        if self.opt_verbose.lower() == "on":
            msg = "self.insert_sql:{}"
            logger.info(msg.format(self.insert_sql))

    # 
    def insert_csv_data_tosqlite(self,list_noise_s_3quest_values, pt_db_sqlite, conn):
                
        ''' 
        INFO: list_noise_s_3quest_values:[['pub', 'pub', 'pub', 'pub'], ['SMOS', 'NMOS', 'GMOS', 'delta_SNR'], ['2.840550', '4.154481', '2.914813', '29.453750']]
        INFO: list_noise_s_3quest_values:[['AVG', 'AVG', 'AVG', 'AVG'], ['SMOS', 'NMOS', 'GMOS', 'delta_SNR'], ['3.358136', '4.220144', '3.328679', '24.638061']]
        ''' 
        noise = list_noise_s_3quest_values[0][0]        
        msg = "noise:{}"
        logger.info(msg.format(noise))    

        # chose insert table sql
        self.select_insert_tab_sql(noise)    

        ''' 
        list_noise_3quest_values = ['2.840550', '4.154481', '2.914813', '29.453750']
        ''' 
        # prepare noise, dut_foldername, insert_date, insert_time
        list_noise_3quest_values = list_noise_s_3quest_values[2]
        list_noise_3quest_values.insert(len(list_noise_3quest_values), self.noise)
        list_noise_3quest_values.insert(len(list_noise_3quest_values), self.dut_foldername)
        list_noise_3quest_values.insert(len(list_noise_3quest_values), self.insert_date)
        list_noise_3quest_values.insert(len(list_noise_3quest_values), self.insert_time)

        if self.opt_verbose.lower() == "on":
            msg = "list_noise_3quest_values:{}"
            logger.info(msg.format(list_noise_3quest_values))

        ''' 
        cause 
        INFO: Error occurred: Incorrect number of bindings supplied. The current statement uses 7, and there are 8 supplied.

        so net list [list_noise_3quest_values]
        ''' 
        msg = "[list_noise_3quest_values]:{}"
        logger.info(msg.format( [list_noise_3quest_values] ))
        
        # Insert total lists to sqlite directly
        pt_db_sqlite.create_csv3quest_many(conn, [list_noise_3quest_values])
                        
        # Save (commit) the changes daily
        conn.commit()    

    def insert_noise_file_tosqlite(self, pt_db_sqlite, conn):
        self.insert_sql=sql_insert_table_noise_type
        
        if self.opt_verbose.lower() == "on":
            msg = "self.insert_sql:{}"
            logger.info(msg.format(self.insert_sql))
            msg = "len(self.list_noise_file): {}"
            logger.info(msg.format(len(self.list_noise_file) ))

        '''    
        Python: Number of rows affected by cursor.execute("SELECT …)
        https://stackoverflow.com/questions/2511679/python-number-of-rows-affected-by-cursor-executeselect
        '''        
        try:
            c = conn.cursor()
            c.execute(sql_query_table_noise_type_count)
            (number_of_rows_noise_type, )=c.fetchone()
        except Error as e:
            msg = "Error create_table:{}"
            logger.info(msg.format(e))    

        if number_of_rows_noise_type < len(self.list_noise_file): # If previous number less than current one       
            msg = "number_of_rows_noise_type: {} < len(self.list_noise_file):{}; update noise type"
            logger.info(msg.format(number_of_rows_noise_type, len(self.list_noise_file)))    

            # Insert total lists to sqlite directly
            pt_db_sqlite.create_csv3quest_many(conn, self.list_noise_file)

            # Save (commit) the changes daily
            conn.commit()    

    # To prevent dulpicate 3Quest data to insert
    def insert_3quest_path_tosqlite(self, pt_db_sqlite, conn):
        sql_query_table_3Quest_path_count="SELECT COUNT(*) FROM _3Quest_path WHERE path Like '"+\
                                            self.path_dut+"';"
        
        try:
            c = conn.cursor()
            c.execute(sql_query_table_3Quest_path_count)
            (number_of_rows_3Quest_path, )=c.fetchone()
        except Error as e:
            msg = "Error create_table:{}"
            logger.info(msg.format(e)) 
        
        if self.opt_verbose.lower() == "on":
            msg = "sql_query_table_3Quest_path_count:{}"
            logger.info(msg.format(sql_query_table_3Quest_path_count))
            

        if number_of_rows_3Quest_path < 1: # Insert if not exists
            self.insert_sql=sql_insert_table_3Quest_path

            if self.opt_verbose.lower() == "on":
                msg = "self.insert_sql:{}"
                logger.info(msg.format(self.insert_sql))

            # Insert total lists to sqlite directly
            pt_db_sqlite.create_csv3quest_many(conn, [[self.path_dut]])

            # Save (commit) the changes daily
            conn.commit()     

        return number_of_rows_3Quest_path            
            
    def delete_table_chariot_csv_throughput(self,conn, id):
        """
        Delete a tseotcdaily by Chariot_CSV_Throughput id
        :param conn:  Connection to the SQLite database
        :param id: id of the tseotcdaily
        :return:
        """
        sql = 'DELETE FROM Chariot_CSV_Throughput WHERE id=?'
        cur = conn.cursor()
        cur.execute(sql, (id,))

    def delete_table_chariot_csv_throughput_all(self,conn):
        """
        Delete all rows in the Chariot_CSV_Throughput table
        :param conn: Connection to the SQLite database
        :return:
        """
        sql = 'DELETE FROM Chariot_CSV_Throughput'
        cur = conn.cursor()
        cur.execute(sql)

        print('Delete all rows in Table Chariot_CSV_Throughput.')    