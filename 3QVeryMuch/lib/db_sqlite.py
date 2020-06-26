# 2020/03/08 Initial
#################################################
import os,sys,logging,time
import csv,re

import json, yaml
import sqlite3
from sqlite3 import Error

from logger import logger

sql_query_WiFi_DHCP_Avg = """ SELECT DISTINCT char_log.test_method, char_log.model, char_log.fw, 
                                char_csv.csv_foldername, char_csv.csv_filename, char_csv.throughput_avg
                                FROM Chariot_CSV_Throughput char_csv 
                                INNER JOIN Chariot_Log char_log ON char_csv.csv_foldername = char_log.csv_foldername  
                                WHERE char_csv.csv_filename REGEXP  '^Client[0-9]' and  char_log.test_method REGEXP  '^DHCP'
                                ORDER BY char_csv.csv_foldername ASC
                            ); """
sql_insert_table_3Quest_pub = ''' INSERT INTO _3Quest_pub(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_road = ''' INSERT INTO _3Quest_road(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_crossroad = ''' INSERT INTO _3Quest_crossroad(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_train = ''' INSERT INTO _3Quest_train(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_car = ''' INSERT INTO _3Quest_car(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_cafeteria = ''' INSERT INTO _3Quest_cafeteria(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_mensa = ''' INSERT INTO _3Quest_mensa(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_callcenter = ''' INSERT INTO _3Quest_callcenter(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_voice_distractor = ''' INSERT INTO _3Quest_voice_distractor(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_nobgn = ''' INSERT INTO _3Quest_nobgn(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?) '''
sql_insert_table_3Quest_AVG = ''' INSERT INTO _3Quest_AVG(
                                        SMOS,
                                        NMOS,
                                        GMOS,
                                        delta_SNR,
                                        dut_foldername,
                                        insert_date,                                        
                                        insert_time)
                    VALUES(?,?,?,?,?,?,?) '''

class DB_sqlite:
    def __init__(self, path_db_file, dut_foldername, insert_date, insert_time, opt_verbose='OFF'):
        self.path_db_file = path_db_file
        self.dut_foldername = dut_foldername
        self.insert_date = insert_date
        self.insert_time = insert_time
        self.opt_verbose = opt_verbose

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

    #
    def select_insert_tab_sql(self,noise):
        if re.search(r'pub', noise): self.insert_sql=sql_insert_table_3Quest_pub
        if re.search(r'road', noise): self.insert_sql=sql_insert_table_3Quest_road
        if re.search(r'crossroad', noise): self.insert_sql=sql_insert_table_3Quest_crossroad
        if re.search(r'train', noise): self.insert_sql=sql_insert_table_3Quest_train
        if re.search(r'car', noise): self.insert_sql=sql_insert_table_3Quest_car
        if re.search(r'cafeteria', noise): self.insert_sql=sql_insert_table_3Quest_cafeteria
        if re.search(r'mensa', noise): self.insert_sql=sql_insert_table_3Quest_mensa
        if re.search(r'callcenter', noise): self.insert_sql=sql_insert_table_3Quest_callcenter
        if re.search(r'voice_distractor', noise): self.insert_sql=sql_insert_table_3Quest_voice_distractor
        if re.search(r'nobgn', noise): self.insert_sql=sql_insert_table_3Quest_nobgn
        if re.search(r'AVG', noise): self.insert_sql=sql_insert_table_3Quest_AVG

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
        list_noise_3quest_values = list_noise_s_3quest_values[2]
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

    def insert_chariot_log_tosqlite(self,list_list_all_txt_row_target_key_value, pt_db_sqlite, conn):
        # Insert total lists to sqlite directly
        pt_db_sqlite.create_chariotlog_many(conn, list_list_all_txt_row_target_key_value)
                        
        # Save (commit) the changes daily
        conn.commit()    

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