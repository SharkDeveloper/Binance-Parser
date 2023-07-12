from src import *

def main():
    #try:
    tin_usdt_rub_DB = Work_with_Table_PostgreSQL()
    #except Exception as Ex:
    #    print(Ex)
    bank = "Тинькофф" #добавить необходимые банки
    currency = ["USDT","RUB"]
    translator = Translator()
    bank_eng_name = str(translator.translate(bank, "English")).lower()#перевод названия банка на англ тк posgres не чиает русский
    table_name = bank_eng_name + "_"+currency[0]+"_"+currency[1]
    #парсинг
    order_data = Binance_parser(currency[0],currency[1],bank)
    tup = order_data.get_orders()
    #БД
    tin_usdt_rub_DB.create_table(table_name)
    #tup = (("2021-01-16 20:00:00","12","112","54","465","64"),("2021-01-16 20:00:00","12","112","54","465","64"))
    tin_usdt_rub_DB.set_data(table_name,tup)


if __name__ == "__main__":
    main()