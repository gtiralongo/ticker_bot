from  colorama import Fore, Back, Style, init
from binance.client import Client
import pandas as pd
import requests
import smtplib
import config
import json

def credentials():
    return  Client(config.API_KEY, config.API_SECRET, tld='com')

URL = "https://scanner.tradingview.com/crypto/scan"
exchange='BINANCE'
client = credentials()
INDICATORS = ["Recommend.Other","Recommend.All","Recommend.MA","RSI","RSI[1]","Stoch.K","Stoch.D","Stoch.K[1]","Stoch.D[1]","CCI20","CCI20[1]","ADX","ADX+DI","ADX-DI","ADX+DI[1]","ADX-DI[1]","AO","AO[1]","Mom","Mom[1]","MACD.macd","MACD.signal","Rec.Stoch.RSI","Stoch.RSI.K","Rec.WR","W.R","Rec.BBPower","BBPower","Rec.UO","UO","close","EMA5","SMA5","EMA10","SMA10","EMA20","SMA20","EMA30","SMA30","EMA50","SMA50","EMA100","SMA100","EMA200","SMA200","Rec.Ichimoku","Ichimoku.BLine","Rec.VWMA","VWMA","Rec.HullMA9","HullMA9","Pivot.M.Classic.S3","Pivot.M.Classic.S2","Pivot.M.Classic.S1","Pivot.M.Classic.Middle","Pivot.M.Classic.R1","Pivot.M.Classic.R2","Pivot.M.Classic.R3","Pivot.M.Fibonacci.S3","Pivot.M.Fibonacci.S2","Pivot.M.Fibonacci.S1","Pivot.M.Fibonacci.Middle","Pivot.M.Fibonacci.R1","Pivot.M.Fibonacci.R2","Pivot.M.Fibonacci.R3","Pivot.M.Camarilla.S3","Pivot.M.Camarilla.S2","Pivot.M.Camarilla.S1","Pivot.M.Camarilla.Middle","Pivot.M.Camarilla.R1","Pivot.M.Camarilla.R2","Pivot.M.Camarilla.R3","Pivot.M.Woodie.S3","Pivot.M.Woodie.S2","Pivot.M.Woodie.S1","Pivot.M.Woodie.Middle","Pivot.M.Woodie.R1","Pivot.M.Woodie.R2","Pivot.M.Woodie.R3","Pivot.M.Demark.S1","Pivot.M.Demark.Middle","Pivot.M.Demark.R1", "open", "P.SAR", "BB.lower", "BB.upper", "AO[2]", "volume", "change", "low", "high"]

init(autoreset=True)

class Color:
    VERDE = '\033[1;92m' #GREEN 1;
    AMARILLO = '\033[1;93m' #YELLOW 1;
    ROJO = '\033[1;91m' #RED 1;
    NEGRO = '\033[1;90m'
    BLANCO = '\033[1;89m'
    AZUL = '\033[1;94m'
    VIOLETA = '\033[1;95m'
    CYAN = '\033[1;96m'
    RESET = '\033[0m' #RESET COLOR'


def symbol_info(symbolTicker):
    info = client.get_symbol_info(symbolTicker)
    minPrice = info["filters"][0]["minPrice"]
    minQty = info["filters"][2]["minQty"]
    n_minPrice = 0
    n_minQty = 0
    for i in minQty:
        if i == '0':
            n_minQty+=1
        if i== '1':
            break
    for i in minPrice:
        if i == '0':
            n_minPrice+=1
        if i== '1':
            break
    return {"minQty":n_minQty,"minPrice":n_minPrice}

def get_trend(symbolTicker, graf_temp):
    
    decimal = 8
    temp = graf_temp
    if graf_temp == '5m':
        temp = client.get_historical_klines(symbolTicker, Client.KLINE_INTERVAL_5MINUTE, '1 hour ago UTC')
    elif graf_temp == '15m':
        temp = client.get_historical_klines(symbolTicker, Client.KLINE_INTERVAL_15MINUTE, '4 hours ago UTC')
    elif graf_temp == '4h':
        temp = client.get_historical_klines(symbolTicker, Client.KLINE_INTERVAL_4HOUR, '4 days ago UTC')
    elif graf_temp == '1d':
        temp = client.get_historical_klines(symbolTicker, Client.KLINE_INTERVAL_1DAY, '10 days ago UTC')
    elif graf_temp == '1w':
        temp = client.get_historical_klines(symbolTicker, Client.KLINE_INTERVAL_1WEEK, '67 days ago UTC')

    p_open = []
    p_high = []
    p_low = []
    p_close = []
    p_vol = []

    for kline in temp:
        p_open.append(round(float(kline[1]),decimal))
        p_high.append(round(float(kline[2]),decimal))
        p_low.append(round(float(kline[3]),decimal))
        p_close.append(round(float(kline[4]),decimal))
        p_vol.append(round(float(kline[5]),decimal))

    ### Creacion de DataFrame ###
    pd_tendencia=pd.DataFrame([p_open,p_high,p_low,p_close,p_vol],index=['open','high','low','close','vol']).T
    pd_tendencia['open_dif'] = pd_tendencia['open'].diff()
    pd_tendencia['high_dif'] = pd_tendencia['high'].diff()
    pd_tendencia['low_dif'] = pd_tendencia['low'].diff()
    pd_tendencia['close_dif'] = pd_tendencia['close'].diff()
    pd_tendencia['vol_dif'] = pd_tendencia['vol'].diff()

    tendencias = {'open':round(pd_tendencia['open_dif'].sum(),decimal),
                'high':round(pd_tendencia['high_dif'].sum(),decimal),
                'low':round(pd_tendencia['low_dif'].sum(),decimal),
                'close':round(pd_tendencia['close_dif'].sum(),decimal),
                'vol':round(pd_tendencia['vol'].sum(),decimal)
                }

    close_up = tendencias['close']>tendencias['open'] #BULLISH
    close_down = tendencias['close']<tendencias['open']#BEARISH
    high_up = tendencias['high']>tendencias['low'] #BULLISH FLUCTUATION
    high_down = tendencias['high']<tendencias['low']#BEARISH FLUCTUATION
    trend = 'NO TREND'
    ## todo mayor que 0 ##
    if tendencias['close'] > 0 and tendencias['open'] > 0 and tendencias['high'] > 0 and tendencias['low'] > 0:
        if close_up and high_up:
            trend = 'STRONG BULLISH'
        elif close_down and high_down:
            trend = 'POSSIBLE TREND CHANGE TO BEARISH'
        elif close_up and high_down:
            trend = 'BULLISH'
        elif close_down and high_up:
            trend = 'WEAK BULLISH UP FLUCTUATION'
    ## todo menor que 0 ##
    elif tendencias['close'] < 0 and tendencias['open'] < 0 and tendencias['high'] < 0 and tendencias['low'] < 0:
        if close_up and high_up:
            trend = 'POSSIBLE TREND CHANGE TO BULLISH'
        elif close_down and high_down:
            trend = 'STRONG BEARISH'
        elif close_up and high_down:
            trend = 'WEAK BEARISH DOWN FLUCTUATION'
        elif close_down and high_up:
            trend = 'BEARISH'
    ### solo low mayor que 0 ###
    elif tendencias['close'] < 0 and tendencias['open'] < 0 and tendencias['high'] < 0 and tendencias['low'] > 0:
        if close_down and high_down:
            trend = 'A LOT OF BUYS'
        elif close_up and high_down:
            trend = 'WEAK BULLISH'
    ### solo low menor que 0 ###
    elif tendencias['close'] > 0 and tendencias['open'] > 0 and tendencias['high'] > 0 and tendencias['low'] < 0:
        if close_up and high_up:
            trend = 'BULLISH'
        elif close_down and high_up:
            trend = 'WEAK BEARISH'
    ### solo close menor que 0 ###
    elif tendencias['close'] < 0 and tendencias['open'] > 0 and tendencias['high'] > 0 and tendencias['low'] > 0:
        if close_down and high_down:
            trend = 'BEARISH'
        elif close_down and high_up:
            trend = 'WEAK BEARISH'
    ### solo close mayor que 0 ###
    elif tendencias['close'] > 0 and tendencias['open'] < 0 and tendencias['high'] < 0 and tendencias['low'] < 0:
        if close_up and high_up:
            trend = 'BULLISH'
        elif close_up and high_down:
            trend = 'WEAK BULLISH'
    ### solo open menor que 0 ###
    elif tendencias['close'] > 0 and tendencias['open'] < 0 and tendencias['high'] > 0 and tendencias['low'] > 0:
        if close_up and high_up:
            trend = 'BULLISH'
        elif close_up and high_down:
            trend = 'BULLISH FLUCTUATION'
    ### solo open mayor que 0 ###
    elif tendencias['close'] < 0 and tendencias['open'] > 0 and tendencias['high'] < 0 and tendencias['low'] < 0:
        if close_down and high_down:
            trend = 'BEARISH'
        elif close_down and high_up:
            trend = 'BEARISH FLUCTUATION'
    ### solo high menor que 0 ###
    elif tendencias['close'] > 0 and tendencias['open'] > 0 and tendencias['high'] < 0 and tendencias['low'] > 0:
        if close_down and high_down:
            trend = 'BEARISH'
        elif close_up and high_down:
            trend = 'WEAK BULLISH'
    ### solo high mayor que 0 ###
    elif tendencias['close'] < 0 and tendencias['open'] < 0 and tendencias['high'] > 0 and tendencias['low'] < 0:
        if close_up and high_up:
            trend = 'BULLISH'
        elif close_down and high_up:
            trend = 'A LOT OF SALES'
    ### solo high y close menor que 0 ###
    elif tendencias['close'] < 0 and tendencias['open'] > 0 and tendencias['high'] < 0 and tendencias['low'] > 0:
        if close_down and high_down:
            trend = 'BEARISH'
    ### solo high y close mayor que 0 ###
    elif tendencias['close'] > 0 and tendencias['open'] < 0 and tendencias['high'] > 0 and tendencias['low'] < 0:
        if close_up and high_up:
            trend = 'BULLISH'
    ### solo high y open menor que 0 ###
    elif tendencias['close'] > 0 and tendencias['open'] < 0 and tendencias['high'] < 0 and tendencias['low'] > 0:
        if close_up and high_down:
            trend = 'LOW TREND CHANGE TO BEARISH'
    ### solo high y open mayor que 0 ###
    elif tendencias['close'] < 0 and tendencias['open'] > 0 and tendencias['high'] > 0 and tendencias['low'] < 0:
        if close_down and high_up:
            trend = 'POSSIBLE TREND CHANGE TO BEARISH'
    ### solo low y close menor que 0 ###
    elif tendencias['close'] < 0 and tendencias['open'] > 0 and tendencias['high'] > 0 and tendencias['low'] < 0:
        if close_down and high_down:
            trend = 'POSSIBLE TREND CHANGE TO BULLISH'
    ### solo low y close mayor que 0 ###
    elif tendencias['close'] > 0 and tendencias['open'] < 0 and tendencias['high'] < 0 and tendencias['low'] > 0:
        if close_up and high_down:
            trend = 'LOW TREND CHANGE TO BEARISH'
    ### solo low y open menor que 0 ###
    elif tendencias['close'] > 0 and tendencias['open'] < 0 and tendencias['high'] > 0 and tendencias['low'] < 0:
        if close_up and high_up:
            trend = 'WEAK BULLISH'
    ### solo low y open mayor que 0 ###
    elif tendencias['close'] < 0 and tendencias['open'] > 0 and tendencias['high'] < 0 and tendencias['low'] > 0:
        if close_down and high_down:
            trend = 'WEAK BEARISH'
    ### solo close y open mayor que 0 ###
    elif tendencias['close'] > 0 and tendencias['open'] > 0 and tendencias['high'] < 0 and tendencias['low'] < 0:
        if close_up and high_up:
            trend = 'BULLISH DOWN FLUCTUATION'
        elif close_down and high_down:
            trend = 'WEAK BEARISH'
        elif close_up and high_down:
            trend = 'BULLISH DOWN FLUCTUATION'
        elif close_down and high_up:
            trend = 'WEAK BEARISH DOWN FLUCTUATION'
    ### solo close y open menor que 0 ###
    elif tendencias['close'] < 0 and tendencias['open'] < 0 and tendencias['high'] > 0 and tendencias['low'] > 0:
        if close_up and high_up:
            trend = 'WEAK BULLISH UP FLUCTUATION'
        elif close_down and high_down:
            trend = 'BEARISH UP FLUCTUATION'
        elif close_up and high_down:
            trend = 'WEAK BEARISH UP FLUCTUATION'
        elif close_down and high_up:
            trend = 'BEARISH UP FLUCTUATION'
    else:
        trend = 'NO TREND'

    tendencias.update({'trend': trend})

    return tendencias

def get_indicator_temp(symbolTicker,temp):
    if temp == '1m':
        temp_indicator = '|1'
    elif temp == '5m':
        temp_indicator = '|5'
    elif temp == '15m':
        temp_indicator = '|15'
    elif temp == '30m':
        temp_indicator = '|30'
    elif temp == '1h':
        temp_indicator = '|60'
    elif temp == '4h':
        temp_indicator = '|240'
    elif temp == '1w':
        temp_indicator = '|1W'
    elif temp == '1M':
        temp_indicator = '|1M'
    else:
        temp_indicator = ''
    
    indicator_list = []
    
    for i in INDICATORS:
        indicator_list.append(f'{i}{temp_indicator}')
    
    oportunidad = {}
    prelist_temporalidad = {}
    data = {'symbols': {'tickers': [f'BINANCE:{symbolTicker}'] },
            'columns': [i for i in indicator_list]}
    headers = {'User-Agent': 'gustavo/2.0'}
    response = requests.post(URL,json=data, headers=headers, timeout=None)
    if response.status_code != 200:
        raise Exception(f"Algo salio mal. Code {response.status_code}.")
    pre_result = json.loads(response.text)["data"]
    loc_indicator = 0
    for i in pre_result:
        sym = i['s'][8:]
        result = i['d']
        for e in INDICATORS:
            prelist_temporalidad.update({f'{e}': result[loc_indicator]})
            loc_indicator += 1
        oportunidad.update({sym: prelist_temporalidad})

    return oportunidad

def lastprice(symbolTicker):
    tickers = credentials().get_ticker()
    for i in tickers:
        if i['symbol'] == symbolTicker:
            return i['askPrice']

def get_order_bug():
    info_order = {}
    with open('ordenes.json', 'r') as fp:
        data = json.load(fp)
    for i in data.keys():
        info_order = {
                "order_id":data["order_id"],
                "side":data["side"],
                "origQty":float(data["origQty"]),
                "quantity":float(data["quantity"]),
                "price":float(data["price"]),
                "total":float(data["total"]),
                "symbolTicker":data["symbolTicker"],
                "status":data["status"],
                }
        break
    fp.close()
    return info_order

def save_info(info, file):
    with open(file, 'r') as fp:
        data = json.load(fp)
    data.update(info)
    with open(file, 'w') as fp:
        json.dump(data , fp)
    fp.close()

def get_save_info(file):
    with open(file, 'r') as fp:
        data = json.load(fp)
    fp.close()
    return data

def get_status(symbolTicker,orderId):
    return credentials().get_order(symbol=symbolTicker,orderId=orderId)

def info_temp_trade(graf_temp):
    
    info_temp = {}
    if graf_temp == '1d':
        temp_up = '1w'
        porcent_gan = 50
        stop_sell = [(1-(porcent_gan*0.0020)) , (1-(porcent_gan*(0.0020-0.001)))]
        stop_buy = [1.007, 1.0068]
        porcent_temp = [1.04, 1.05]
        porcent_stop = 10
    elif graf_temp == '4h':
        temp_up = '1d'
        porcent_gan = 18
        stop_sell = [(1-(porcent_gan*0.0020)) , (1-(porcent_gan*(0.0020-0.001)))]
        stop_buy = [1.006, 1.0058]
        porcent_temp = [1.01, 1.02]
        porcent_stop = 4
    elif graf_temp == '1h':
        temp_up = '4h'
        porcent_gan = 6
        stop_sell = [(1-(porcent_gan*0.0020)) , (1-(porcent_gan*(0.0020-0.001)))]
        stop_buy = [1.005, 1.0048]
        porcent_temp = [1.007, 1.009]
        porcent_stop = 2.5
    elif graf_temp == '15m':
        temp_up = '4h'
        porcent_gan = 5
        stop_sell = [(1-(porcent_gan*0.0020)) , (1-(porcent_gan*(0.0020-0.001)))]
        stop_buy = [1.004, 1.0038]
        porcent_temp = [1.004, 1.005]
        porcent_stop = 1.5
    elif graf_temp == '5m':
        temp_up = '1h'
        porcent_gan = 1.1
        stop_sell = [(1-(porcent_gan*0.0020)) , (1-(porcent_gan*(0.0020-0.001)))]
        stop_buy = [1.003, 1.0028]
        porcent_temp = [1.0015, 1.0025]
        porcent_stop = 0.55
    info_temp.update({'temp_up': temp_up,'porcent_gan': porcent_gan,'stop_sell': stop_sell,'stop_buy': stop_buy,'porcent_temp': porcent_temp,'porcent_stop': porcent_stop})
    return info_temp

def alerta(datos, symbolTicker):
    mensaje = f'🚀 Operacion: {datos["side"]}\nPrecio📊: {datos["price"]}\n{symbolTicker[:-4]}: {datos["quantity"]}\nUSDT 💵: {datos["total"]}\nOrder ID : {datos["order_id"]}'
    if datos["side"] == "BUY":
        asunto = f'⚠ Operacion de {datos["side"]} 📈 Completada'
    else:
        asunto = f'⚠ Operacion de {datos["side"]} 📉 Completada'     
    mensaje = f'Subject:{asunto}\n\n{mensaje}'
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(config.MAIL, config.PASSWORD)
    server.sendmail("tiralongogus@gmail.com", "gustavotiralongo@gmail.com" , mensaje)
    server.quit()
    telegram_bot(mensaje)
    print(f"Correo enviado")

def telegram_bot(bot_message):
    
    send_text = 'https://api.telegram.org/bot' +config.BOT_TOKEN + '/sendMessage?chat_id=' + config.BOT_CHATID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)

    return response.json()

def all_order(ticker,status="FILLED"):
    order = client.get_all_orders(symbol=ticker)
    orders={}
    num = 1
    for o in order:
        if o["status"] == status:
            time = datetime.datetime.fromtimestamp( o["time"]/1000).strftime('%Y-%m-%d %H:%M:%S')
            orders.update({num:{"symbol": o["symbol"],"price": o["price"],"origQty": o["origQty"],"executedQty": o["executedQty"], "status": o["status"],"type": o["type"],"side": o["side"],"orderId": o["orderId"],"time": time}})
            num += 1
    return orders
