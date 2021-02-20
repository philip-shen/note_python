
Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [Remodel](#remodel)
   * [1: drop_fork](#1-drop_fork)
      * [<a href="https://github.com/Runbook/runbook/blob/master/src/web/tests/base.py">database.py</a>](#databasepy)
   * [2: setUp](#2-setup)
   * [3: rethink_make_tables](#3-rethink_make_tables)
   * [4: start](#4-start)
   * [5: <strong>init</strong>](#5-init)
   * [6: connect_rethink](#6-connect_rethink)
   * [8: get_parser](#8-get_parser)
   * [9: match_database_duplicate_strains](#9-match_database_duplicate_strains)
   * [10: setup](#10-setup)
   * [11: dispose](#11-dispose)
   * [12: create_table](#12-create_table)
   * [13: remove_old_days](#13-remove_old_days)
   * [14: fetch](#14-fetch)
   * [15: insert](#15-insert)
   * [16: last_known_blocks](#16-last_known_blocks)
   * [17: get_table](#17-get_table)
   * [18: tearDown](#18-teardown)
   * [19: createTable](#19-createtable)
   * [20: rethink_empty_db](#20-rethink_empty_db)
   * [21: <strong>init</strong>](#21-init)
   * [22: get_args](#22-get_args)
   * [23: check_server_up](#23-check_server_up)
   * [24: _create_database](#24-_create_database)
   * [25: _create_table](#25-_create_table)
   * [26: check_table_exists](#26-check_table_exists)
   * [27: backup_local](#27-backup_local)
   * [28: export_json](#28-export_json)
   * [29: count_documents](#29-count_documents)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)



# Purpose  
Take a note of RethinkDB.

# Remodel 
[ linkyndy /remodel ](https://github.com/linkyndy/remodel)  


# 1: drop_fork 
[Python rethinkdb.db方法代碼示例](https://vimsky.com/zh-tw/examples/detail/python-method-rethinkdb.db.html)

```
開發者ID:hyperledger，項目名稱:sawtooth-marketplace，代碼行數:23，代碼來源:database.py
```
## [database.py](https%3A%2F%2Fgithub.com%2FRunbook%2Frunbook%2Fblob%2Fmaster%2Fsrc%2Fweb%2Ftests%2Fbase.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def drop_fork(self, block_num):
        """Deletes all resources from a particular block_num
        """
        block_results = r.db(self._name).table('blocks')\
            .filter(lambda rsc: rsc['block_num'].ge(block_num))\
            .delete()\
            .run(self._conn)

        resource_results = r.db(self._name).table_list()\
            .for_each(
                lambda table_name: r.branch(
                    r.eq(table_name, 'blocks'),
                    [],
                    r.eq(table_name, 'auth'),
                    [],
                    r.db(self._name).table(table_name)
                    .filter(lambda rsc: rsc['start_block_num'].ge(block_num))
                    .delete()))\
            .run(self._conn)

        return {k: v + resource_results[k] for k, v in block_results.items()} 
```


# 2: setUp  
```
開發者ID:Runbook，項目名稱:runbook，代碼行數:24，代碼來源:base.py
```
## [base.py](https%3A%2F%2Fgithub.com%2FRunbook%2Frunbook%2Fblob%2Fmaster%2Fsrc%2Fweb%2Ftests%2Fbase.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def setUp(self):
        try:
            g.rdb_conn = r.connect(
                host=app.config['DBHOST'], port=app.config['DBPORT'],
                auth_key=app.config['DBAUTHKEY'], db=app.config['DATABASE'])

            userdata = {
                'username': 'test@tester.com',
                'email': 'test@tester.com',
                'password': 'password456',
                'company': 'company',
                'contact': 'tester'
            }

            # Create test user
            user = User()
            user.config = app.config
            user.createUser(userdata, g.rdb_conn)

        except RqlDriverError:
            # If no connection possible throw 503 error
            abort(503, "No Database Connection Could be Established.") 
```


# 3: rethink_make_tables  
```
開發者ID:man-group，項目名稱:pytest-plugins，代碼行數:19，代碼來源:rethink.py
```
## [rethink.py](https%3A%2F%2Fgithub.com%2Fman-group%2Fpytest-plugins%2Fblob%2Fmaster%2Fpytest-server-fixtures%2Fpytest_server_fixtures%2Frethink.py)


```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def rethink_make_tables(request, rethink_module_db):
    """ Module-scoped fixture that creates all tables specified in the test
        module attribute FIXTURE_TABLES.

    """
    reqd_table_list = getattr(request.module, 'FIXTURE_TABLES')
    log.debug("Do stuff before all module tests with {0}".format(reqd_table_list))
    conn = rethink_module_db
    for table_name, primary_key in reqd_table_list:
        try:
            rethinkdb.db(conn.db).table_create(table_name,
                                               primary_key=primary_key,
                                               ).run(conn)
            log.info('Made table "{0}" with key "{1}"'
                     .format(table_name, primary_key))
        except rethinkdb.errors.RqlRuntimeError as err:
            log.debug('Table "{0}" not made: {1}'.format(table_name, err.message)) 
```


# 4: start  
```
開發者ID:morpheus65535，項目名稱:bazarr，代碼行數:20，代碼來源:rethinkdb.py
```
## [rethinkdb.py](https%3A%2F%2Fgithub.com%2Fmorpheus65535%2Fbazarr%2Fblob%2Fmaster%2Flibs%2Fapscheduler%2Fjobstores%2Frethinkdb.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def start(self, scheduler, alias):
        super(RethinkDBJobStore, self).start(scheduler, alias)

        if self.client:
            self.conn = maybe_ref(self.client)
        else:
            self.conn = r.connect(db=self.database, **self.connect_args)

        if self.database not in r.db_list().run(self.conn):
            r.db_create(self.database).run(self.conn)

        if self.table not in r.table_list().run(self.conn):
            r.table_create(self.table).run(self.conn)

        if 'next_run_time' not in r.table(self.table).index_list().run(self.conn):
            r.table(self.table).index_create('next_run_time').run(self.conn)

        self.table = r.db(self.database).table(self.table) 
```


# 5: __init__  
```
開發者ID:APSL，項目名稱:kaneda，代碼行數:18，代碼來源:rethink.py
```
## [rethink.py](https%3A%2F%2Fgithub.com%2FAPSL%2Fkaneda%2Fblob%2Fmaster%2Fkaneda%2Fbackends%2Frethink.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def __init__(self, db, table_name=None, connection=None, host=None, port=None, user=None, password=None,
                 timeout=0.3):
        if not r:
            raise ImproperlyConfigured('You need to install the rethinkdb library to use the RethinkDB backend.')
        if connection:
            self.connection = connection
        elif host and port:
            if user and password:
                self.connection = r.connect(host=host, port=port, db=db, user=user, password=password, timeout=timeout)
            else:
                self.connection = r.connect(host=host, port=port, db=db, timeout=timeout)
        self.db = db
        self.table_name = table_name
        if self.connection is None:
            self.connection = r.connect(db=db, timeout=timeout)
        self._create_database() 
```


# 6: connect_rethink  
```
開發者ID:nextstrain，項目名稱:fauna，代碼行數:20，代碼來源:rethink_io.py
```

## [rethink_io.py](https://github.com/nextstrain/fauna/blob/master/base/rethink_io.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def connect_rethink(self, db, rethink_host='localhost', auth_key=None, **kwargs):
        '''
        Connect to rethink database,
        '''
        if rethink_host == 'localhost':
            try:
                conn = r.connect(host=rethink_host, port=28015, db=db).repl()
                print("Connected to the \"" + db + "\" database")
                return conn
            except:
                raise Exception("Failed to connect to the database, " + db)
        else:
            try:
                conn = r.connect(host=rethink_host, port=28015, db=db, auth_key=auth_key).repl()
                print("Connected to the \"" + db + "\" database")
                return conn
            except:
                raise Exception("Failed to connect to the database, " + db) 
```


# 8: get_parser  
```
開發者ID:nextstrain，項目名稱:fauna，代碼行數:21，代碼來源:dengue_download.py 
```
## [dengue_download.py](https://github.com/nextstrain/fauna/blob/master/tdb/dengue_download.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def get_parser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-db', '--database', default='tdb', help="database to download from")
    parser.add_argument('--rethink_host', default=None, help="rethink host url")
    parser.add_argument('--auth_key', default=None, help="auth_key for rethink database")
    parser.add_argument('--local', default=False, action="store_true",  help ="connect to local instance of rethinkdb database")
    parser.add_argument('-v', '--virus', default='dengue', help="virus name")
    parser.add_argument('--subtype', help="subtype to be included in download")
    parser.add_argument('--ftype', default='tsv', help="output file format, default \"tsv\", options are \"json\" and \"tsv\"")
    parser.add_argument('--fstem', default=None, help="default output file name is \"VirusName_Year_Month_Date\"")
    parser.add_argument('--path', default='data', help="path to dump output files to")

    parser.add_argument('--select', nargs='+', type=str, default=[], help="Select specific fields ie \'--select field1:value1 field2:value1,value2\'")
    parser.add_argument('--present', nargs='+', type=str, default=[], help="Select specific fields to be non-null ie \'--present field1 field2\'")
    parser.add_argument('--interval', nargs='+', type=str, default=[], help="Select interval of values for fields \'--interval field1:value1,value2 field2:value1,value2\'")
    parser.add_argument('--years_back', type=str, default=None, help='number of past years to sample sequences from \'--years_back field:value\'')
    parser.add_argument('--relaxed_interval', default=False, action="store_true", help="Relaxed comparison to date interval, 2016-XX-XX in 2016-01-01 - 2016-03-01")
    return parser 
```


# 9: match_database_duplicate_strains  
```
開發者ID:nextstrain，項目名稱:fauna，代碼行數:18，代碼來源:upload.py
```
## [upload.py](https://github.com/nextstrain/fauna/blob/master/vdb/upload.py)  

```

```


# 10: setup  
```
開發者ID:smartsdk，項目名稱:ngsi-timeseries-api，代碼行數:6，代碼來源:rethink.py
```
## [rethink.py](https%3A%2F%2Fgithub.com%2Fsmartsdk%2Fngsi-timeseries-api%2Fblob%2Fmaster%2Fsrc%2Ftranslators%2Frethink.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def setup(self):
        self.conn = rt.connect(self.host, self.port)
        # rt.db(self.db_name).table_drop(self.TABLE_NAME).run(self.conn)
        self.create_table() 
```


# 11: dispose
```
開發者ID:smartsdk，項目名稱:ngsi-timeseries-api，代碼行數:5，代碼來源:rethink.py
```
## [rethink.py](https%3A%2F%2Fgithub.com%2Fsmartsdk%2Fngsi-timeseries-api%2Fblob%2Fmaster%2Fsrc%2Ftranslators%2Frethink.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def dispose(self):
        rt.db(self.db_name).table_drop(self.TABLE_NAME).run(self.conn)
        self.conn.close() 
```


# 12: create_table  
```
開發者ID:smartsdk，項目名稱:ngsi-timeseries-api，代碼行數:6，代碼來源:rethink.py
```
[rethink.py](https%3A%2F%2Fgithub.com%2Fsmartsdk%2Fngsi-timeseries-api%2Fblob%2Fmaster%2Fsrc%2Ftranslators%2Frethink.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def create_table(self):
        res = rt.db(self.db_name).table_create(self.TABLE_NAME).run(self.conn)
        if res['tables_created'] != 1:
            raise RuntimeError("Could not create table '{}'".format(self.TABLE_NAME)) 
```


# 13: remove_old_days  
```
開發者ID:uwescience，項目名稱:TrafficCruising-DSSG2017，代碼行數:36，代碼來源:remove_old_days.py
```
[remove_old_days.py](https%3A%2F%2Fgithub.com%2Fuwescience%2FTrafficCruising-DSSG2017%2Fblob%2Fmaster%2Fpipeline%2Fremove_old_days.py)  

```

```


# 14: fetch  
```
開發者ID:hyperledger，項目名稱:sawtooth-marketplace，代碼行數:7，代碼來源:database.py
```
[database.py](https%3A%2F%2Fgithub.com%2Fhyperledger%2Fsawtooth-marketplace%2Fblob%2Fmaster%2Fledger_sync%2Fmarketplace_ledger_sync%2Fdatabase.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def fetch(self, table_name, primary_id):
        """Fetches a single resource by its primary id
        """
        return r.db(self._name).table(table_name)\
            .get(primary_id).run(self._conn) 
```


# 15: insert
```
開發者ID:hyperledger，項目名稱:sawtooth-marketplace，代碼行數:7，代碼來源:database.py
```
[database.py](https%3A%2F%2Fgithub.com%2Fhyperledger%2Fsawtooth-marketplace%2Fblob%2Fmaster%2Fledger_sync%2Fmarketplace_ledger_sync%2Fdatabase.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def insert(self, table_name, docs):
        """Inserts a document or a list of documents into the specified table
        in the database
        """
        return r.db(self._name).table(table_name).insert(docs).run(self._conn) 
```


# 16: last_known_blocks
```
開發者ID:hyperledger，項目名稱:sawtooth-marketplace，代碼行數:7，代碼來源:database.py
```
[database.py](https%3A%2F%2Fgithub.com%2Fhyperledger%2Fsawtooth-marketplace%2Fblob%2Fmaster%2Fledger_sync%2Fmarketplace_ledger_sync%2Fdatabase.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def last_known_blocks(self, count):
        """Fetches the ids of the specified number of most recent blocks
        """
        cursor = r.db(self._name).table('blocks')\
            .order_by('block_num')\
            .get_field('block_id')\
            .run(self._conn)

        return list(cursor)[-count:] 
```


# 17: get_table  
```
開發者ID:hyperledger，項目名稱:sawtooth-marketplace，代碼行數:7，代碼來源:database.py
```
[database.py](https%3A%2F%2Fgithub.com%2Fhyperledger%2Fsawtooth-marketplace%2Fblob%2Fmaster%2Fledger_sync%2Fmarketplace_ledger_sync%2Fdatabase.py)  

```

```


# 18: tearDown  
```
開發者ID:Runbook，項目名稱:runbook，代碼行數:13，代碼來源:base.py
```
[base.py](https%3A%2F%2Fgithub.com%2FRunbook%2Frunbook%2Fblob%2Fmaster%2Fsrc%2Fweb%2Ftests%2Fbase.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def tearDown(self):
        # why the need to reconnect?
        g.rdb_conn = r.connect(
            host=app.config['DBHOST'], port=app.config['DBPORT'],
            auth_key=app.config['DBAUTHKEY'], db=app.config['DATABASE'])
        r.db('crdb').table('users').delete().run(g.rdb_conn)
        try:
            g.rdb_conn.close()
        except AttributeError:
            # Who cares?
            pass 
```


# 19: createTable  
```
開發者ID:Runbook，項目名稱:runbook，代碼行數:10，代碼來源:create_db.py
```
[create_db.py]https%3A%2F%2Fgithub.com%2FRunbook%2Frunbook%2Fblob%2Fmaster%2Fsrc%2Fbridge%2Fmgmtscripts%2Fcreate_db.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def createTable(dbname, tablename, conn):
    ''' Create a rethinkDB table '''
    print("Creating table: %s") % tablename
    try:
        r.db(dbname).table_create(tablename).run(conn)
    except (RqlDriverError, RqlRuntimeError, socket.error) as e:
        print("RethinkDB Error: %s") % e.message
        print("Table %s not created") % tablename 
```


# 20: rethink_empty_db  
```
開發者ID:man-group，項目名稱:pytest-plugins，代碼行數:17，代碼來源:rethink.py
```
[rethink.py](https%3A%2F%2Fgithub.com%2Fman-group%2Fpytest-plugins%2Fblob%2Fmaster%2Fpytest-server-fixtures%2Fpytest_server_fixtures%2Frethink.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def rethink_empty_db(request, rethink_module_db, rethink_make_tables):
    """ Function-scoped fixture that will empty all the tables defined
        for the `rethink_make_tables` fixture.

        This is a useful approach, because of the long time taken to
        create a new RethinkDB table, compared to the time to empty one.
    """
    tables_to_emptied = (table[0] for table
                         in getattr(request.module, 'FIXTURE_TABLES'))
    conn = rethink_module_db

    for table_name in tables_to_emptied:
        rethinkdb.db(conn.db).table(table_name).delete().run(conn)
        log.debug('Emptied "{0}" before test'.format(table_name))
    yield conn 
```


# 21: __init__  
```
開發者ID:man-group，項目名稱:pytest-plugins，代碼行數:17，代碼來源:rethink.py
```
[rethink.py](https%3A%2F%2Fgithub.com%2Fman-group%2Fpytest-plugins%2Fblob%2Fmaster%2Fpytest-server-fixtures%2Fpytest_server_fixtures%2Frethink.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def __init__(self, **kwargs):
        # defer loading of rethinkdb
        global rethinkdb
        import rethinkdb

        super(RethinkDBServer, self).__init__(**kwargs)
        self._driver_port = self._get_port(28015)
        self._cluster_port = self._get_port(29015)
        self._http_port = self._get_port(8080)
        self.db = None 
```


# 22: get_args  
```
開發者ID:man-group，項目名稱:pytest-plugins，代碼行數:14，代碼來源:rethink.py
```
[rethink.py](https%3A%2F%2Fgithub.com%2Fman-group%2Fpytest-plugins%2Fblob%2Fmaster%2Fpytest-server-fixtures%2Fpytest_server_fixtures%2Frethink.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def get_args(self, **kwargs):
        cmd = [
            '--bind', self._listen_hostname,
            '--driver-port', str(self.port),
            '--http-port', str(self.http_port),
            '--cluster-port', str(self.cluster_port),
        ]

        if 'workspace' in kwargs:
            cmd += ['--directory', str(kwargs['workspace'] / 'db')]

        return cmd 
```


# 23: check_server_up  
```
開發者ID:man-group，項目名稱:pytest-plugins，代碼行數:14，代碼來源:rethink.py
```
[rethink.py](https%3A%2F%2Fgithub.com%2Fman-group%2Fpytest-plugins%2Fblob%2Fmaster%2Fpytest-server-fixtures%2Fpytest_server_fixtures%2Frethink.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def check_server_up(self):
        """Test connection to the server."""
        log.info("Connecting to RethinkDB at {0}:{1}".format(
            self.hostname, self.port))

        if not self.hostname:
            return False

        try:
            self.conn = rethinkdb.connect(host=self.hostname,
                                          port=self.port, db='test')
            return True
        except rethinkdb.RqlDriverError as err:
            log.warning(err)
        return False 
```


# 24: _create_database  
```
開發者ID:APSL，項目名稱:kaneda，代碼行數:5，代碼來源:rethink.py
```
[rethink.py](https%3A%2F%2Fgithub.com%2FAPSL%2Fkaneda%2Fblob%2Fmaster%2Fkaneda%2Fbackends%2Frethink.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def _create_database(self):
        if self.db not in r.db_list().run(self.connection):
            r.db_create(self.db).run(self.connection) 
```


# 25: _create_table  
```
開發者ID:APSL，項目名稱:kaneda，代碼行數:5，代碼來源:rethink.py
```
[rethink.py](https%3A%2F%2Fgithub.com%2FAPSL%2Fkaneda%2Fblob%2Fmaster%2Fkaneda%2Fbackends%2Frethink.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def _create_table(self, metric):
        table_name = self._get_table_name(metric)
        if table_name not in r.db(self.db).table_list().run(self.connection):
            r.db(self.db).table_create(table_name).run(self.connection) 
```


# 26: check_table_exists  
```
開發者ID:nextstrain，項目名稱:fauna，代碼行數:9，代碼來源:rethink_io.py
```
[rethink_io.py](https%3A%2F%2Fgithub.com%2Fnextstrain%2Ffauna%2Fblob%2Fmaster%2Fbase%2Frethink_io.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def check_table_exists(self, database, table):
        '''
        Check for existing table
        '''
        existing_tables = r.db(database).table_list().run()
        if table not in existing_tables:
            raise Exception("No table exists yet for " + table + " available are " + str(existing_tables)) 
```


# 27: backup_local  
```
開發者ID:nextstrain，項目名稱:fauna，代碼行數:17，代碼來源:rethink_interact.py
```

[rethink_interact.py](https%3A%2F%2Fgithub.com%2Fnextstrain%2Ffauna%2Fblob%2Fmaster%2Fbase%2Frethink_interact.py)  
```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def backup_local(self, database, path='', delete_expired=False, **kwargs):
        '''
        make backup of every table in database, store locally
        '''
        print("Backing up " + database + " on " + self.rethink_io.get_upload_date() + " to location: " + path)
        if not os.path.isdir(path):
            os.makedirs(path)
        tables = r.db(database).table_list().run()
        for table in tables:
            dump_file = self.rethink_io.get_upload_date() + '_' + database + '_' + table + '.tar.gz'
            self.dump(database=database, dump_table=table, dump_file=dump_file, **kwargs)
            shutil.move(dump_file, path+'/'+dump_file)
            print("Successfully backed up " + table)
        if delete_expired:
            self.delete_expired_local_backups(path=path, **kwargs) 
```


# 28: export_json  
```
開發者ID:nextstrain，項目名稱:fauna，代碼行數:15，代碼來源:rethink_interact.py
```

[rethink_interact.py](https%3A%2F%2Fgithub.com%2Fnextstrain%2Ffauna%2Fblob%2Fmaster%2Fbase%2Frethink_interact.py)  
```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def export_json(self, directory, json_file, export_database, export_table, **kwargs):
        '''
        export export_database.export_table to backup_file
        '''
        print("Exporting database: " + export_database + ", table: " + export_table + ", to file: " + json_file)
        if os.path.isdir(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)
        try:
            documents = list(r.db(export_database).table(export_table).run())
            write_json(documents, json_file)
        except:
            raise Exception("Couldn't export " + export_database + '.' + export_table + " to " + directory) 
```


# 29: count_documents  
```
開發者ID:nextstrain，項目名稱:fauna，代碼行數:7，代碼來源:download.py
```

[download.py](https%3A%2F%2Fgithub.com%2Fnextstrain%2Ffauna%2Fblob%2Fmaster%2Ftdb%2Fdownload.py)  

```
# 需要導入模塊: import rethinkdb [as 別名]
# 或者: from rethinkdb import db [as 別名]
def count_documents(self):
        '''
        return integer count of number of documents in table
        '''
        return r.db(self.database).table(self.virus).count().run() 
```

