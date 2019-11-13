import configparser
import os
import psycopg2

def dbase_connect(password):
    try:
        config = configparser.ConfigParser()
        dir = os.path.dirname(os.path.abspath(__file__))
        config.read(dir + os.sep + 'config.ini')
        connection = psycopg2.connect(user = "postgres",
                                  password = password,
                                  host = "127.0.0.1",
                                  port = "5432" )
        connection.autocommit = True
        cursor = connection.cursor()
        create_database = '''CREATE DATABASE listdir_db
                            WITH 
                            OWNER = postgres
                            ENCODING = 'UTF8'
                            LC_COLLATE = 'English_Philippines.1252'
                            LC_CTYPE = 'English_Philippines.1252'
                            TABLESPACE = pg_default
                            CONNECTION LIMIT = -1;'''

        #cursor.execute("CREATE DATABASE ")
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
