import requests
from bs4 import BeautifulSoup
import json
from DataBase import Work_with_Table_PostgreSQL


class parser:
  """Делает запрос сайта и переводит в json для дальнейшей обработки"""
  def __init__(self,url,data,headers) -> None:
    self.url = url
    self.data = data
    self.headers = headers

  def get_html_website(self):
    """Получет сайт и переводит в json формат"""
    website = requests.post(url = self.url,headers = self.headers,json = data)#запрос сайта
    soup = BeautifulSoup(website.text,"lxml")
    #print(site.text)
    data = soup.text.replace("<html><body><p>","")#removing excess
    data = data.replace("</p></body></html>","")#removing excess
    data = json.loads(data)# json converter
    return data
  
class Binance_parser(parser):
  """Парсит json с Binance P2P и добавляет в БД"""
  def __init__(self,currency) -> None:
    super().__init__(self.url, self.data, self.headers)
    self.url = url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    self.data = {
      "asset": currency[0],
      "fiat": currency[1],
      "merchantCheck": False,
      "page": 1,
      "payTypes": ["TinkoffNew"],
      "publisherType": None,
      "rows": 10,
      "tradeType": "BUY"
      #transAmount: "1000" # объем 
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
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.3.787 Yowser/2.5 Safari/537.36",
    "x-trace-id":"9511b3e7-39d9-478d-9c5d-acfab3894548",
    "x-ui-request-trace":"9511b3e7-39d9-478d-9c5d-acfab3894548"
    }


  def get_orders_from_database(data):
    count = 0

    for i in range(0,len(data['data'])):
      for j in range(0,len(data['data'][i]['adv']['tradeMethods'])):
        if data['data'][i]['adv']['tradeMethods'][j]["tradeMethodName"] == "Тинькофф":
          count+=1
          print(count,data['data'][i]['adv']['price'])#print price"""
  
  




data =  [
  {"adv": {"advNo": "11390890296054288384", "classify": "mass", "tradeType": "SELL", "asset": "USDT",
  "fiatUnit": "RUB", "advStatus": None, "priceType": None, "priceFloatingRatio": None, "rateFloatingRatio": None,
  "currencyRate": None, "price": "66.40", "initAmount": None, "surplusAmount": "1858.02",
  "amountAfterEditing": None, "maxSingleTransAmount": "125000.00", "minSingleTransAmount": "2000.00", 
  "buyerKycLimit": None, "buyerRegDaysLimit": None, "buyerBtcPositionLimit": None, "remarks": None, 
  "autoReplyMsg": "", "payTimeLimit": None, "tradeMethods": [{"payId": None, "payMethodId": "", "payType": None,
  "payAccount": None, "payBank": None, "paySubBank": None, "identifier": "RUBfiatbalance", "iconUrlColor": None,
  "tradeMethodName": "BinancePay (RUB)", "tradeMethodShortName": "Фиатный баланс RUB", 
  "tradeMethodBgColor": "#D89F00"}, 

  {"payId": None, "payMethodId": "", "payType": None, "payAccount": None, "payBank": None, "paySubBank": None, 
  "identifier": "Advcash", "iconUrlColor": None, "tradeMethodName": "AdvCash", "tradeMethodShortName": "AdvCash",
  "tradeMethodBgColor": "#00B27A"}, {"payId": None, "payMethodId": "", "payType": None, "payAccount": None,
  "payBank": None, "paySubBank": None, "identifier": "Payeer", "iconUrlColor": None, 
  "tradeMethodName": "Payeer", "tradeMethodShortName": "Payeer", "tradeMethodBgColor": "#03A9F4"}],
  "userTradeCountFilterTime": None, "userBuyTradeCountMin": None, "userBuyTradeCountMax": None, 
  "userSellTradeCountMin": None, "userSellTradeCountMax": None, "userAllTradeCountMin": None, 
  "userAllTradeCountMax": None, "userTradeCompleteRateFilterTime": None, "userTradeCompleteCountMin": None,
  "userTradeCompleteRateMin": None, "userTradeVolumeFilterTime": None, "userTradeType": None, 
  "userTradeVolumeMin": None, 
  "userTradeVolumeMax": None, "userTradeVolumeAsset": None, "createTime": None, "advUpdateTime": None,
  "fiatVo": None, "assetVo": None, "advVisibleRet": None, "assetLogo": None, "assetScale": 2, 
  "fiatScale": 2, "priceScale": 2, "fiatSymbol": "₽", "isTradable": True, 
  "dynamicMaxSingleTransAmount": "123249.27", "minSingleTransQuantity": "30.12", 
  "maxSingleTransQuantity": "1882.53", "dynamicMaxSingleTransQuantity": "1856.16", "tradableQuantity": "1856.16", 
  "commissionRate": "0.00100000", "tradeMethodCommissionRates": [], "launchCountry": None, 
  "abnormalStatusList": None, "closeReason": None}, "advertiser": 
  {"userNo": "sfeac0adf165233628d4d9057ae498411", "realName": None, "nickName": "Torgash365", 
  "margin": None, "marginUnit": None, "orderCount": None, "monthOrderCount": 274, "monthFinishRate": 1.0,
  "advConfirmTime": None, "email": None, "registrationTime": None, "mobile": None, "userType": "user",
  "tagIconUrls": [], "userGrade": 2, "userIdentity": "", "proMerchant": None, "isBlocked": None}}
  ]