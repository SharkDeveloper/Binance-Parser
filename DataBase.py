import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import user,password


class Create_DB_PostgreSQL:
    def __init__(self) -> None:
        self.connection = psycopg2.connect(user = user,password = password,host = "127.0.0.1", port = "5432",database="binance_p2p_db")
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)    
        self.cursor = self.connection.cursor()
        self.create_database()

    def create_database(self):
        create_database_query = "CREATE DATABASE IF NOT EXISTS binance_p2p_db"
        self.cursor.execute(create_database_query)

class Work_with_Table_PostgreSQL(Create_DB_PostgreSQL):
    """Все для подключения,создания и добавления БД,Таблиц в PostgerSQL"""
    def __init__(self) -> None:
        super().__init__(self)

    def create_table(self):
        create_table_query = "CREATE TABLE IF NOT EXISTS TIN_USDT_RUB (DTIME TIMESTAMP  ,PRICE REAL,  AMOUNT REAL, MIN REAL,MAX REAL, ORDERS_COMPLITED INTEGER);"
        self.cursor.execute(create_table_query)
        

    def set_table(self,Table, DTIME,  PRICE, AMOUNT, MIN, MAX, ORDERS_COMPLITED):
        tup = (DTIME,PRICE,AMOUNT,MIN,MAX,ORDERS_COMPLITED)
        insert_query = f" INSERT INTO {Table} ( DTIME,  PRICE, AMOUNT, MIN, MAX, ORDERS_COMPLITED)VALUES (?,?,?,?,?,?);"
        #insert_query = "INSERT INTO Test1 (ID) VALUES (2);"
        self.cursor.executemany(insert_query,tup)
        print("Записи добавлены в Binance_p2p_db") 

    def drop_table(self,Table):
        self.cursor.execute(f"DROP TABLE {Table};")

    