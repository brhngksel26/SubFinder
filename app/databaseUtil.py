from multiprocessing import connection
import psycopg2 as db
from psycopg2 import Error
import confuse
from app.decorators import *
from psycopg2.extras import *




def selectQueryFetchone(query):

    try:
        source = confuse.YamlSource('/home/burhan/projects/SubFinder/config.yaml')

        dbConnectionString = source["database"]["dbConnectionString"]
        print(dbConnectionString)
        
        connection = db.connect(dbConnectionString)

        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute(query)

        result = cursor.fetchone()


    except (Exception , Error) as error:
        Log(f"Select Query {error}","error")
        print(error)
    
    finally:
        if (connection):
            cursor.close()
            connection.close()

        return result


def selectQueryFetchall(query):

    try:
        source = confuse.YamlSource('/home/burhan/projects/SubFinder/config.yaml')

        dbConnectionString = source["database"]["dbConnectionString"]
        print(dbConnectionString)
        
        connection = db.connect(dbConnectionString)

        cursor = connection.cursor(cursor_factory=DictCursor)

        cursor.execute(query)

        result = cursor.fetchall()


    except (Exception , Error) as error:
        Log(f"Select Query {error}","error")
        print(error)
    
    finally:
        if (connection):
            cursor.close()
            connection.close()

        return result
    
    

def insertQuery(query):

    source = confuse.YamlSource('/home/burhan/projects/SubFinder/config.yaml')

    dataBaseConfig = source["database"]

    dbConnectionString = dataBaseConfig["dbConnectionString"]
        
    with db.connect(dbConnectionString) as connection:

        cursor = connection.cursor()
        cursor.execute(query)
            

    return "Success"

