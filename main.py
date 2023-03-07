from DataBase import PostgreSQL_DB
from Binance_Parser import Binance_parser

def main():
    tin_usdt_rub_DB = PostgreSQL_DB()
    tin_usdt_rub_DB.set_data("TIN_USDT_RUB","20:00","2021-01-16","12","112","54","465","64")
    order_data = Binance_parser(["USDT","RUB"])
    
if __name__ == "__main__":
    main()