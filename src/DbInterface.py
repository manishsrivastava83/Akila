#!/usr/bin/python
from tornado.ioloop import IOLoop
from tornado import gen
import tormysql
import uuid
#import mysql.connector as mariadb

class DBConnection(object):
     __shared_state = {}
     def __init__(self):
        self.__dict__ = self.__shared_state
        try:
            self.mariadbConnectionPool = tormysql.ConnectionPool(
                max_connections = 20, #max open connections
                idle_seconds = 7200, #conntion idle timeout time, 0 is not timeout
                wait_connection_timeout = 3, #wait connection timeout
                host = "127.0.0.1",
                user = "root",
                passwd = "manishs",
                db = "akila",
                charset = "utf8"
                )
        except mariadb.Error as error:
            #TOFO LOG error handle error
            print("Error: {}".format(error))

     @gen.coroutine
     def executeInsertQuery(self,insertQuery,valueList):
        with (yield self.mariadbConnectionPool.Connection()) as conn:
            try:
                with conn.cursor() as cursor:
                    print("Executing insertQuery %s %s ",insertQuery,valueList)
                    #print(valueList)
                    #yield cursor.execute(insertQuery,valueList)
                    #yield cursor.execute("INSERT INTO business_accounts (oid_index,businessAccountUID) VALUES ( '%s','%s' ) ",tup)
                    yield cursor.execute(insertQuery, valueList)
                    print("Executed insertQuery %s %s",insertQuery,valueList)
            except TypeError as error:
                print("Error: {}".format(error))
            except IndexError as error:
                print("Error: {}".format(error))
            except:
                print("Unexpected error:")
                yield conn.rollback()
            else:
                yield conn.commit()


class QueryGateway(object):
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
        self.dbConnection=DBConnection()
        self.statementMap = {}
        self.statementMap["insert_business_accounts"] = "INSERT INTO business_accounts (oid_index,businessAccountUID,businessEntityName,EIN,firstName,middleName,lastName,emailID,password,contactNumber,address,city,country,zipCode) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        self.statementMap["store_message_from_twillio"] = "INSERT INTO messages ( message_uuid,source, destination, message_content, message_time, session_id) VALUES ( %s,%s,%s,%s,%s,%s )"
        #self.statementMap["insert_business_accounts_test"] = "INSERT INTO business_accounts (oid_index, businessAccountUID) VALUES ( %s, %s)"
    
    @gen.coroutine
    def insertBAN(self,valueList):
        yield self.dbConnection.executeInsertQuery(self.statementMap["insert_business_accounts"],valueList)

    @gen.coroutine
    def storeMessageFromTwillio(self,valueList):
        yield self.dbConnection.executeInsertQuery(self.statementMap["store_message_from_twillio"],valueList)
#queryGateway=QueryGateway()
#ioloop = IOLoop.instance()
#ioloop.run_sync(lambda : queryGateway.insertBAN((str(1),str(uuid.uuid1()))))
#ioloop.run_sync(lambda : queryGateway.insertBAN({'1','2','3','4','5','6','7','8','9','10','11','12','13','14'}))
