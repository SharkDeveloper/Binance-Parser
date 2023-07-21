import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


"""Делает запрос сайта и переводит в json для дальнейшей обработки"""
class Binance_parser:
  def __init__(self,currency_asset,currency_fiat,bank) -> None:
    self.url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    self.bank = bank
    
    self.data = {
      "proMerchantAds":False,
       "page":1,
       "rows":10,
       "payTypes":[],
       "countries":[],
       "asset":currency_asset,
       "fiat":currency_fiat,
       "tradeType":"BUY" # объем 
    }
    
    self.headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language":"ru,en;q=0.9",
    "bnc-uuid":"678df1b9-d680-42e6-9881-753b30203ef6",
    "c2ctype":"c2c_merchant",
    "clienttype":"web",
    "content-type":"application/json",
    "csrftoken":"a937cc2a67f45280d31994ed162ae13f",
    "device-info":"eyJzY3JlZW5fcmVzb2x1dGlvbiI6Ijg2NCwxNTM2IiwiYXZhaWxhYmxlX3NjcmVlbl9yZXNvbHV0aW9uIjoiODI0LDE1MzYiLCJzeXN0ZW1fdmVyc2lvbiI6IldpbmRvd3MgMTAiLCJicmFuZF9tb2RlbCI6InVua25vd24iLCJzeXN0ZW1fbGFuZyI6InJ1IiwidGltZXpvbmUiOiJHTVQrMyIsInRpbWV6b25lT2Zmc2V0IjotMTgwLCJ1c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwMi4wLjUwMDUuMTY3IFlhQnJvd3Nlci8yMi43LjMuNzg3IFlvd3Nlci8yLjUgU2FmYXJpLzUzNy4zNiIsImxpc3RfcGx1Z2luIjoiUERGIFZpZXdlcixDaHJvbWUgUERGIFZpZXdlcixDaHJvbWl1bSBQREYgVmlld2VyLE1pY3Jvc29mdCBFZGdlIFBERiBWaWV3ZXIsV2ViS2l0IGJ1aWx0LWluIFBERiIsImNhbnZhc19jb2RlIjoiMTllYWFjOWUiLCJ3ZWJnbF92ZW5kb3IiOiJHb29nbGUgSW5jLiAoQU1EKSIsIndlYmdsX3JlbmRlcmVyIjoiQU5HTEUgKEFNRCwgQU1EIFJhZGVvbihUTSkgR3JhcGhpY3MgRGlyZWN0M0QxMSB2c181XzAgcHNfNV8wLCBEM0QxMSkiLCJhdWRpbyI6IjEyNC4wNDM0NzUyNzUxNjA3NCIsInBsYXRmb3JtIjoiV2luMzIiLCJ3ZWJfdGltZXpvbmUiOiJFdXJvcGUvTW9zY293IiwiZGV2aWNlX25hbWUiOiJZYW5kZXggVjIyLjcuMy43ODcgKFdpbmRvd3MpIiwiZmluZ2VycHJpbnQiOiIyNjU0MTA3NjY3YTI1ODg4MWUxYjg2OGY4MTBiYjdmMyIsImRldmljZV9pZCI6IiIsInJlbGF0ZWRfZGV2aWNlX2lkcyI6IjE2NjU2OTg1MTM0MDd1d2NKUXM0R1JiTVlBa0Rhb3hjIn0=",
    "fvideo-id":"33de2d42f317a8f49cad7970bc63d948cdf788ea",
    "lang":"ru",
    "origin":"https://p2p.binance.com",
    "referer":"https://p2p.binance.com/ru/trade/all-payments/USDT?fiat=RUB",
    "sec-ch-ua":'"Not A;Brand";v="99", "Chromium";v="102", "Yandex";v="22"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest":"empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.4.777 Yowser/2.5 Safari/537.36",
    "x-trace-id":"9511b3e7-39d9-478d-9c5d-acfab3894548",
    "x-ui-request-trace":"9511b3e7-39d9-478d-9c5d-acfab3894548"
    }
    
  """Парсит json с Binance P2P и подготавливает формат для БД"""
  def get_orders(self):
    """Получет сайт и переводит в json формат"""
    try:
      website = requests.post(url = self.url,headers = self.headers,json = self.data)#запрос сайта
      soup = BeautifulSoup(website.text,"lxml")
      orders_data = soup.text.replace("<html><body><p>","")#removing excess
      orders_data = orders_data.replace("</p></body></html>","")#removing excess
      orders_data = json.loads(orders_data)# json converter
      self.orders_data = orders_data
    except:
      print("Не удалось подключиться к сайту!\nПроверьте интенет соединение...")
    data = self.orders_data
    all_orders = list()


    for i in range(0,len(data['data'])):
      #for j in range(0,len(data['data'][i]['adv']['tradeMethods'])):
      #  if data['data'][i]['adv']['tradeMethods'][j]["tradeMethodName"] == self.bank: 
      print(data["data"][i]['adv'])

      amount = data["data"][i]['adv']['tradableQuantity']
      price = data['data'][i]['adv']['price']
      Min = data["data"][i]['adv']["minSingleTransAmount"]
      Max = data["data"][i]['adv']["maxSingleTransAmount"]
      orders_complited = data["data"][i]['advertiser']['monthOrderCount']
      orders_rate = data["data"][i]['advertiser']['monthFinishRate']#процентное соотношение выполненных заказов
      tup = (datetime.now(),price,amount,Min,Max,orders_complited,orders_rate)
      all_orders.append(tup)
    return all_orders
  def get_bank():
    #class="bn-sdd-list css-2rl2kr"
    return 0
  def get_crypto_currency():
    return 0
  def get_fiat_currency():
    return 0
  
  


a = {'advNo': '11471854627184660480', 'classify': 'mass', 'tradeType': 'SELL', 
     'asset': 'USDT', 'fiatUnit': 'RUB', 'advStatus': None, 'priceType': None, 
     'priceFloatingRatio': None, 'rateFloatingRatio': None, 'currencyRate': None, 
     'price': '78.25', 'initAmount': None, 'surplusAmount': '144.81', 
     'amountAfterEditing': None, 'maxSingleTransAmount': '15924.00', 
     'minSingleTransAmount': '500.00', 'buyerKycLimit': None, 'buyerRegDaysLimit': None, 
     'buyerBtcPositionLimit': None, 'remarks': None, 'autoReplyMsg': '', 'payTimeLimit': None, 
     'tradeMethods': [{'payId': None, 'payMethodId': '', 'payType': None, 'payAccount': None, 
                       'payBank': None, 'paySubBank': None, 'identifier': 'RUBfiatbalance', 
                       'iconUrlColor': None, 'tradeMethodName': 'BinancePay (RUB)', 
                       'tradeMethodShortName': 'Фиатный баланс RUB', 
                       'tradeMethodBgColor': '#D89F00'}], 'userTradeCountFilterTime': None, 
                       'userBuyTradeCountMin': None, 'userBuyTradeCountMax': None, 
                       'userSellTradeCountMin': None, 'userSellTradeCountMax': None, 
                       'userAllTradeCountMin': None, 'userAllTradeCountMax': None, 
                       'userTradeCompleteRateFilterTime': None, 'userTradeCompleteCountMin': None, 
                       'userTradeCompleteRateMin': None, 'userTradeVolumeFilterTime': None, 
                       'userTradeType': None, 'userTradeVolumeMin': None, 'userTradeVolumeMax': None, 
                       'userTradeVolumeAsset': None, 'createTime': None, 'advUpdateTime': None, 
                       'fiatVo': None, 'assetVo': None, 'advVisibleRet': None, 'assetLogo': None, 
                       'assetScale': 2, 'fiatScale': 2, 'priceScale': 2, 'fiatSymbol': '₽', 
                       'isTradable': True, 'dynamicMaxSingleTransAmount': '11320.06', 
                       'minSingleTransQuantity': '6.38', 'maxSingleTransQuantity': '203.50', 
                       'dynamicMaxSingleTransQuantity': '144.66', 'tradableQuantity': '144.66', 
                       'commissionRate': '0.00100000', 'tradeMethodCommissionRates': [], 
                       'launchCountry': None, 'abnormalStatusList': None, 
'closeReason': None, 'storeInformation': None}