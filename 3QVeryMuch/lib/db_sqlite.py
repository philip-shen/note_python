# 2020/03/08 Initial
#################################################
import os,sys,logging,time
import csv,re

import json, yaml
import sqlite3
from sqlite3 import Error
import pandas as pd

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
    
    def str_sql_query_table_3quest_report(self):
        self.sql_query_table_3quest_report=\
            "SELECT DISTINCT noise.name,noise.description as noise, tb_nobgn.SMOS , tb_nobgn.NMOS , tb_nobgn.GMOS , tb_nobgn.delta_SNR, tb_nobgn.dut_foldername, tb_nobgn.insert_date, tb_nobgn.insert_time \
            FROM _3Quest_nobgn tb_nobgn \
            INNER JOIN noise_type noise ON noise.name = tb_nobgn.noise \
            WHERE tb_nobgn.dut_foldername LIKE (?) and tb_nobgn.insert_date LIKE (?) \
            UNION \
            SELECT DISTINCT noise.name,noise.description as noise, tb_pub.SMOS , tb_pub.NMOS , tb_pub.GMOS , tb_pub.delta_SNR, tb_pub.dut_foldername, tb_pub.insert_date, tb_pub.insert_time \
            FROM _3Quest_pub tb_pub \
            INNER JOIN noise_type noise ON noise.name = tb_pub.noise \
            WHERE tb_pub.dut_foldername LIKE (?) and tb_pub.insert_date LIKE (?) \
            UNION \
            SELECT DISTINCT noise.name,noise.description as noise, tb_road.SMOS , tb_road.NMOS , tb_road.GMOS , tb_road.delta_SNR, tb_road.dut_foldername, tb_road.insert_date, tb_road.insert_time \
            FROM _3Quest_road tb_road \
            INNER JOIN noise_type noise ON noise.name = tb_road.noise \
            WHERE tb_road.dut_foldername LIKE (?) and tb_road.insert_date LIKE (?) \
            UNION \
            SELECT DISTINCT noise.name,noise.description as noise, tb_crossroad.SMOS , tb_crossroad.NMOS , tb_crossroad.GMOS , tb_crossroad.delta_SNR, tb_crossroad.dut_foldername, tb_crossroad.insert_date, tb_crossroad.insert_time \
            FROM _3Quest_crossroad tb_crossroad \
            INNER JOIN noise_type noise ON noise.name = tb_crossroad.noise \
            WHERE tb_crossroad.dut_foldername LIKE (?) and tb_crossroad.insert_date LIKE (?) \
            UNION \
            SELECT DISTINCT noise.name,noise.description as noise, tb_train.SMOS , tb_train.NMOS , tb_train.GMOS , tb_train.delta_SNR, tb_train.dut_foldername, tb_train.insert_date, tb_train.insert_time \
            FROM _3Quest_train tb_train \
            INNER JOIN noise_type noise ON noise.name = tb_train.noise \
            WHERE tb_train.dut_foldername LIKE (?) and tb_train.insert_date LIKE (?) \
            UNION \
            SELECT DISTINCT noise.name,noise.description as noise, tb_car.SMOS , tb_car.NMOS , tb_car.GMOS , tb_car.delta_SNR, tb_car.dut_foldername, tb_car.insert_date, tb_car.insert_time \
            FROM _3Quest_car tb_car \
            INNER JOIN noise_type noise ON noise.name = tb_car.noise \
            WHERE tb_car.dut_foldername LIKE (?) and tb_car.insert_date LIKE (?) \
            UNION \
            SELECT DISTINCT noise.name,noise.description as noise, tb_cafeteria.SMOS , tb_cafeteria.NMOS , tb_cafeteria.GMOS , tb_cafeteria.delta_SNR, tb_cafeteria.dut_foldername, tb_cafeteria.insert_date, tb_cafeteria.insert_time \
            FROM _3Quest_cafeteria tb_cafeteria \
            INNER JOIN noise_type noise ON noise.name = tb_cafeteria.noise \
            WHERE tb_cafeteria.dut_foldername LIKE (?) and tb_cafeteria.insert_date LIKE (?) \
            UNION \
            SELECT DISTINCT noise.name,noise.description as noise, tb_mensa.SMOS , tb_mensa.NMOS , tb_mensa.GMOS , tb_mensa.delta_SNR, tb_mensa.dut_foldername, tb_mensa.insert_date, tb_mensa.insert_time \
            FROM _3Quest_mensa tb_mensa \
            INNER JOIN noise_type noise ON noise.name = tb_mensa.noise \
            WHERE tb_mensa.dut_foldername LIKE (?) and tb_mensa.insert_date LIKE (?) \
            UNION \
            SELECT DISTINCT noise.name,noise.description as noise, tb_callcenter.SMOS , tb_callcenter.NMOS , tb_callcenter.GMOS , tb_callcenter.delta_SNR, tb_callcenter.dut_foldername, tb_callcenter.insert_date, tb_callcenter.insert_time \
            FROM _3Quest_callcenter tb_callcenter \
            INNER JOIN noise_type noise ON noise.name = tb_callcenter.noise \
            WHERE tb_callcenter.dut_foldername LIKE (?) and tb_callcenter.insert_date LIKE (?) \
            UNION \
            SELECT DISTINCT noise.name,noise.description as noise, tb_voice_distractor.SMOS , tb_voice_distractor.NMOS , tb_voice_distractor.GMOS , tb_voice_distractor.delta_SNR, tb_voice_distractor.dut_foldername, tb_voice_distractor.insert_date, tb_voice_distractor.insert_time \
            FROM _3Quest_voice_distractor tb_voice_distractor \
            INNER JOIN noise_type noise ON noise.name = tb_voice_distractor.noise \
            WHERE tb_voice_distractor.dut_foldername LIKE (?) and tb_voice_distractor.insert_date LIKE (?) \
            UNION \
            SELECT DISTINCT noise.name,noise.description as noise, tb_AVG.SMOS , tb_AVG.NMOS , tb_AVG.GMOS , tb_AVG.delta_SNR, tb_AVG.dut_foldername, tb_AVG.insert_date, tb_AVG.insert_time \
            FROM _3Quest_AVG tb_AVG \
            INNER JOIN noise_type noise ON noise.name = tb_AVG.noise \
            WHERE tb_AVG.dut_foldername LIKE (?) and tb_AVG.insert_date LIKE (?)"

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
        """ 
        create a table from the create_table_sql statement
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

    def query_3quest_table(self, pt_db_sqlite, conn):
        self.str_sql_query_table_3quest_report()

        if self.opt_verbose.lower() == "on":
            msg = "self.sql_query_table_3quest_report:{}"
            #logger.info(msg.format(self.sql_query_table_3quest_report)) 
            msg = "self.dut_foldername:{}; self.insert_date:{}"
            logger.info(msg.format(self.dut_foldername, self.insert_date))       

        try:
            df_sql_table = pd.read_sql_query(self.sql_query_table_3quest_report, conn, \
                                params=(self.dut_foldername, self.insert_date,\
                                        self.dut_foldername, self.insert_date,\
                                        self.dut_foldername, self.insert_date,\
                                        self.dut_foldername, self.insert_date,\
                                        self.dut_foldername, self.insert_date,\
                                        self.dut_foldername, self.insert_date,\
                                        self.dut_foldername, self.insert_date,\
                                        self.dut_foldername, self.insert_date,\
                                        self.dut_foldername, self.insert_date,\
                                        self.dut_foldername, self.insert_date,\
                                        self.dut_foldername, self.insert_date,))

            #df = df_sql_table.copy()
            self.df_query_3quest_table = df_sql_table.copy()

        except Error as e:
            msg = "Error create_table:{}"
            logger.info(msg.format(e)) 
        
        """ 
            name             noise      SMOS      NMOS      GMOS  delta_SNR                               dut_foldername insert_date insert_time
        0   000             nobgn  3.903344  4.451300  3.827119  28.773125  logitech_0702_noise-18dB_debussy-debug-0701    20200705    16:14:28
        1   001               pub  2.544831  4.215844  2.754500  37.121313  logitech_0702_noise-18dB_debussy-debug-0701    20200705    16:14:28
        2   002              road  2.013450  4.305000  2.464431  42.814312  logitech_0702_noise-18dB_debussy-debug-0701    20200705    16:14:28
        3   003         crossroad  2.858994  4.326850  3.014300  45.056937  logitech_0702_noise-18dB_debussy-debug-0701    20200705    16:14:28
        4   004             train  2.781244  4.358738  2.982506  44.793063  logitech_0702_noise-18dB_debussy-debug-0701    20200705    16:14:28
        5   005               car  3.259744  4.335181  3.284425  46.144687  logitech_0702_noise-18dB_debussy-debug-0701    20200705    16:14:28
        6   006         cafeteria  3.690281  4.305944  3.597819  31.478625  logitech_0702_noise-18dB_debussy-debug-0701    20200705    16:14:28
        7   007             mensa  3.457444  4.252481  3.398813  29.928375  logitech_0702_noise-18dB_debussy-debug-0701    20200705    16:14:28
        8   008        callcenter  3.839938  4.179069  3.666994  28.150125  logitech_0702_noise-18dB_debussy-debug-0701    20200705    16:14:28
        9   009  voice_distractor  3.826412  3.867169  3.529694  22.014875  logitech_0702_noise-18dB_debussy-debug-0701    20200705    16:14:28
        10  010               AVG  3.217568  4.259757  3.252060  35.627544  logitech_0702_noise-18dB_debussy-debug-0701    20200705    16:14:28
        """ 
        
        if self.opt_verbose.lower() == "on":
            msg = "self.df_query_3quest_table:{}"
            logger.info(msg.format(self.df_query_3quest_table))    
    
    def write_to_excel(self):
        path_report_excel = os.path.join(self.path_dut, self.dut_foldername+'.xlsx')

        if self.opt_verbose.lower() == "on":
            msg = "path_report_excel:{}"
            logger.info(msg.format(path_report_excel))

        #self.df_query_3quest_table.to_excel(path_report_excel, index=False, header=False)
        self.df_query_3quest_table.to_excel(path_report_excel, index=False)


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