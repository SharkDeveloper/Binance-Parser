import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from .config.config import psql_password,psql_user


class Create_DB_PostgreSQL:
    def __init__(self) -> None:

        self.connection = psycopg2.connect(user = psql_user ,password = psql_password, port = "5432",database="binance_p2p")
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)    
        self.cursor = self.connection.cursor()
        

    def create_database(self):
        create_database_query = "CREATE DATABASE binance_p2p IF NOT EXISTS"
        self.cursor.execute(create_database_query)

class Work_with_Table_PostgreSQL(Create_DB_PostgreSQL):
    """Все для подключения,создания и добавления БД,Таблиц в PostgerSQL"""
    def __init__(self) -> None:
        super().__init__()

    def create_table(self,table_name):
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name}(DTIME TIMESTAMP  ,PRICE REAL,  AMOUNT REAL, MIN REAL,MAX REAL, ORDERS_COMPLITED INTEGER , ORDERS_RATE REAL);"
        self.cursor.execute(create_table_query)
        print(f"table {table_name} created")

    def set_data(self,Table,tup):
        #(DTIME,PRICE,AMOUNT,MIN,MAX,ORDERS_COMPLITED,ORDERS_RATE)
        insert_query = f" INSERT INTO {Table} VALUES (%s,%s,%s,%s,%s,%s,%s)"
        #insert_query = "INSERT INTO Test1 (ID) VALUES (2);"
        self.cursor.executemany(insert_query,tup)
        print("Записи добавлены в Binance_p2p") 

    def drop_table(self,Table):
        self.cursor.execute(f"DROP TABLE {Table};")

    def create_trademethod_table(self,table_name):
        create_table_query = """CREATE TABLE IF NOT EXISTS TRADEMETHOD 
                                (
                                    tradeMethodName STRING NOT NULL,
                                    tradeMethodShortName STRING NOT NULL,
                                );"""
        self.cursor.execute(create_table_query)
        print("table created")
    