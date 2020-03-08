# 2020/03/08 Initial
#################################################
import twstock
import os,sys,logging,time
import csv,re

import json, yaml
import sqlite3
from sqlite3 import Error

class DB_sqlite:
    def __init__(self, path_db_file):
        self.path_db_file = path_db_file

    def create_connection(self):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(self.path_db_file)
            #print(sqlite3.version)
            return conn
        except Error as e:
            print(e)
        
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
            print(e)

    def create_chariotlog_many(self, conn, list_chariotlog_s):

        sql = ''' INSERT INTO ChariotLog(csv_foldername,
                                        test_method,
                                        case_number,
                                        model,
                                        hw,
                                        fw,
                                        wireless_mode,
                                        frequency,
                                        channel,
                                        country_code,
                                        encryption,
                                        antenna_degree,
                                        test_vendor,
                                        test_client)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) '''
        try:
            cur = conn.cursor()
            # How to insert a list of lists into a table? [Python]
            #https://stackoverflow.com/questions/51503490/how-to-insert-a-list-of-lists-into-a-table-python

            # How do I use prepared statements for inserting MULTIPLE records in SQlite using Python / Django?
            # To use parameterized queries, and to provide more than one set of parameters
            #https://stackoverflow.com/questions/5616895/how-do-i-use-prepared-statements-for-inserting-multiple-records-in-sqlite-using
            list_tuple_chariotlog_s = [tuple(l) for l in list_chariotlog_s]
            #print(list_tuple_tseotcdailyinfo_s)
            cur.executemany(sql, list_tuple_chariotlog_s)

        except sqlite3.Error as err:
            print("Error occurred: %s" % err)
        else:
            print('Total {} record(s) to insert table.'.format(cur.rowcount))
        
        return cur.lastrowid

    '''
    CSV_FolderName:202003061104, CSV_FileName:Client2-W4_Tx_result_1st.csv
    Throughput Avg.(Mbps):155.531, Throughput Min.(Mbps):22.008 ,Throughput Max.(Mbps):39.428
    '''
    def create_csvthruput_many(self, conn, list_csvthruput_s):
        sql = ''' INSERT INTO ChariotLog(csv_foldername,
                                        csv_filename,
                                        throughput_avg,
                                        throughput_min,
                                        throughput_max)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) '''
        try:
            cur = conn.cursor()
            # How to insert a list of lists into a table? [Python]
            #https://stackoverflow.com/questions/51503490/how-to-insert-a-list-of-lists-into-a-table-python

            # How do I use prepared statements for inserting MULTIPLE records in SQlite using Python / Django?
            # To use parameterized queries, and to provide more than one set of parameters
            #https://stackoverflow.com/questions/5616895/how-do-i-use-prepared-statements-for-inserting-multiple-records-in-sqlite-using
            list_tuple_chariotlog_s = [tuple(l) for l in list_chariotlog_s]
            #print(list_tuple_tseotcdailyinfo_s)
            cur.executemany(sql, list_tuple_chariotlog_s)

        except sqlite3.Error as err:
            print("Error occurred: %s" % err)
        else:
            print('Total {} record(s) to insert table.'.format(cur.rowcount))
        
        return cur.lastrowid