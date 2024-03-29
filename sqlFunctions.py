import mysql
import mysql.connector
import pandas as pd
import pymysql
from mysql.connector import Error
from sqlalchemy import create_engine

'''
def connectToDatabase():

    host_name = 'database-1.caxiwm5xesw7.us-east-2.rds.amazonaws.com'
    try:
        connection = mysql.connector.connect(host=host_name,
                                        user='admin', 
                                        password='s6I1H=)2.21a',
                                        port = '3306',
                                        database='Solviing_Prices')
    except:
        print('Connection to DB failed.')
    return connection
'''

def createNewTable(query):

    host_name = 'solviing.com' #'database-1.caxiwm5xesw7.us-east-2.rds.amazonaws.com'
    try:
        connection = mysql.connector.connect(host=host_name,
        user = '8BGSBCAT41cgtzuEmYfPtmNZo', #'admin', 
        password = '}L[%N=Uk<TCh)OZcA%^:Q9BS/', #'s6I1H=)2.21a',
        port = '3306',
        database = 'Solviing_Prices')
    except Exception as e:
        print('Connection to DB failed.')
        print(e)

    mycursor = connection.cursor()
    mycursor.execute(query)

    return

def queryTable(query):
    host_name = 'solviing.com' #'database-1.caxiwm5xesw7.us-east-2.rds.amazonaws.com'
    try:
        conn = mysql.connector.connect(host=host_name,
                                        user = '8BGSBCAT41cgtzuEmYfPtmNZo', #'admin', 
                                        password = '}L[%N=Uk<TCh)OZcA%^:Q9BS/', #'s6I1H=)2.21a',
                                        port = '3306',
                                        database = 'Solviing_Prices')
    except:
        print('Connection to DB failed.')
    
    df = pd.read_sql_query (query, conn)
    
    return df


def performQuery(query):

    host_name = 'solviing.com' #'database-1.caxiwm5xesw7.us-east-2.rds.amazonaws.com'
    try:
        connection = mysql.connector.connect(host=host_name,
                                             user = '8BGSBCAT41cgtzuEmYfPtmNZo', #'admin', 
                                             password = '}L[%N=Uk<TCh)OZcA%^:Q9BS/', #'s6I1H=)2.21a',
                                             port = '3306',
                                            database = 'Solviing_Prices')
    except:
        print('Connection to DB failed.')
     
    try:
        sql_select_Query = query
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        # get all records
        records = cursor.fetchall()
        #print("Total number of rows in table: ", cursor.rowcount)
        return records

    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")
    
    return

def deleteTable(table_name):

    host_name = 'solviing.com' #'database-1.caxiwm5xesw7.us-east-2.rds.amazonaws.com'
    try:
        connection = mysql.connector.connect(host=host_name,
                                        user = '8BGSBCAT41cgtzuEmYfPtmNZo', #'admin', 
                                        password = '}L[%N=Uk<TCh)OZcA%^:Q9BS/', #'s6I1H=)2.21a',
                                        port = '3306',
                                        database = 'Solviing_Prices')
    except:
        print('Connection to DB failed.')

    try:
        sql_select_Query = "DELETE FROM " + table_name
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")


def setInitialConfig():

    host_name = 'solviing.com' #'database-1.caxiwm5xesw7.us-east-2.rds.amazonaws.com'
    try:
        connection = mysql.connector.connect(host=host_name,
                                        user = '8BGSBCAT41cgtzuEmYfPtmNZo', #'admin', 
                                        password = '}L[%N=Uk<TCh)OZcA%^:Q9BS/', #'s6I1H=)2.21a',
                                        port = '3306',
                                        database = 'Solviing_Prices')
    except:
        print('Connection to DB failed.')

    try:
        sql_select_Query = "ALTER TABLE inputs2 MODIFY id_propiedad INT PRIMARY KEY AUTO_INCREMENT"#"DELETE FROM " + table_name
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")


def writeTable(df, table_name):

    try:
        sql_engine = create_engine("mysql+pymysql://{user}:{pw}@solviing.com/{db}"
                                    .format(user = '8BGSBCAT41cgtzuEmYfPtmNZo', #'admin',
                                            pw = '}L[%N=Uk<TCh)OZcA%^:Q9BS/', #'s6I1H=)2.21a',
                                            port = '3306',
                                            db = 'Solviing_Prices'))
        connection = sql_engine#.raw_connection()
        df.to_sql(name=table_name, con=connection, if_exists='append',index = False)

    except Exception as e:
        print('Writing table failed')
        print(e)
    if table_name == 'inputs2':
        setInitialConfig()

def queryOutputs():

    host_name = 'solviing.com' #'database-1.caxiwm5xesw7.us-east-2.rds.amazonaws.com'
    try:
        conn = mysql.connector.connect(host=host_name,
                                        user = '8BGSBCAT41cgtzuEmYfPtmNZo', #'admin', 
                                        password = '}L[%N=Uk<TCh)OZcA%^:Q9BS/', #'s6I1H=)2.21a',
                                        port = '3306',
                                        database = 'Solviing_Prices')
    except:
        print('Connection to DB failed.')
    
    outputs_df = pd.read_sql_query ('''
                                SELECT
                                *
                                FROM outputs2
                                ''', conn)
    outputs_df['colonia'] = outputs_df['colonia'].str.lower()
    return outputs_df

def queryProperties():

    host_name = 'solviing.com' #'database-1.caxiwm5xesw7.us-east-2.rds.amazonaws.com'
    try:
        conn = mysql.connector.connect(host=host_name,
                                        user = '8BGSBCAT41cgtzuEmYfPtmNZo', #'admin', 
                                        password = '}L[%N=Uk<TCh)OZcA%^:Q9BS/', #'s6I1H=)2.21a',
                                        port = '3306',
                                        database = 'Solviing_Prices')
    except:
        print('Connection to DB failed.')
    
    properties_df = pd.read_sql_query ('''
                                SELECT
                                *
                                FROM inputs2
                                ''', conn)
    properties_df['colonia'] = properties_df['colonia'].str.lower()
    return properties_df


def queryPriceCatalogue():

    host_name = 'solviing.com' #'database-1.caxiwm5xesw7.us-east-2.rds.amazonaws.com'
    try:
        conn = mysql.connector.connect(host=host_name,
                                        user = '8BGSBCAT41cgtzuEmYfPtmNZo', #'admin', 
                                        password = '}L[%N=Uk<TCh)OZcA%^:Q9BS/', #'s6I1H=)2.21a',
                                        port = '3306',
                                        database = 'Solviing_Prices')
    except:
        print('Connection to DB failed.')

    price_cat_df = pd.read_sql_query ('''
                                SELECT
                                *
                                FROM prices_catalog_v2
                                ''', conn)
    price_cat_df['colonia'] = price_cat_df['colonia'].str.lower()
    return price_cat_df

def queryRankingCatalogue():

    host_name = 'solviing.com' #'database-1.caxiwm5xesw7.us-east-2.rds.amazonaws.com'
    try:
        conn = mysql.connector.connect(host=host_name,
                                        user = '8BGSBCAT41cgtzuEmYfPtmNZo', #'admin', 
                                        password = '}L[%N=Uk<TCh)OZcA%^:Q9BS/', #'s6I1H=)2.21a',
                                        port = '3306',
                                        database = 'Solviing_Prices')
    except:
        print('Connection to DB failed.')

    ranking_cat_df = pd.read_sql_query ('''
                                SELECT
                                *
                                FROM ranking_catalog_v1
                                ''', conn)
    ranking_cat_df['colonia'] = ranking_cat_df['colonia'].str.lower()
    ranking_cat_df = ranking_cat_df[~(ranking_cat_df['Calificacion_MERCADO'].isna())]
    ranking_cat_df = ranking_cat_df[~(ranking_cat_df['Calificacion_SEGURIDAD'].isna())]
    ranking_cat_df['Calificacion_MERCADO'] = ranking_cat_df['Calificacion_MERCADO'].astype('int')
    ranking_cat_df['Calificacion_SEGURIDAD'] = ranking_cat_df['Calificacion_SEGURIDAD'].astype('int')
    ranking_cat_df['score'] = ranking_cat_df['score'].astype('int')
    
    return ranking_cat_df
