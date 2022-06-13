from alert import telegram_bot
from indicator import *
from colorama import *
import time

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

client = credentials()
# client = Client(config.API_KEY, config.API_SECRET, tld='com')

def dinamic_order_buy(symbolTicker,quan,stop_buy):
    order = {}
    # print(quan)
    # prev_symbolPrice = get_indicator(symbolTicker)['close']
    try:    
        prev_symbolPrice = float(lastprice(symbolTicker)) # get_indicator_temp(symbolTicker)[symbolTicker]['close']
    except:
        time.sleep(2)    
        prev_symbolPrice = float(lastprice(symbolTicker)) # get_indicator_temp(symbolTicker)[symbolTicker]['close']
    try:
        info = symbol_info(symbolTicker)
    except:
        time.sleep(2)
        info = symbol_info(symbolTicker)

    buyOrder = client.create_order(
        symbol = symbolTicker,
        side = 'BUY',
        type = 'STOP_LOSS_LIMIT',
        quantity = float(round(quan["quantityBuy"]/round(prev_symbolPrice*stop_buy[1],2),info["minQty"])),
        price = str(float(round(prev_symbolPrice*stop_buy[0],info["minPrice"]))),
        stopPrice = str(float(round(prev_symbolPrice*stop_buy[1],info["minPrice"]))),
        timeInForce = 'GTC'
    )
    print(f'{Color.AZUL}!!====>Orden Creada<====!!{Color.RESET}') 
    telegram_bot(f'Start dinamic *BUY* order *{symbolTicker}* _{prev_symbolPrice}_')

    on = True
    while on == True:
        time.sleep(10)
        try:
            order_id = buyOrder.get('orderId')
        except:
            time.sleep(2)
            order_id = buyOrder.get('orderId')
        try:
            filled_order=client.get_order(symbol=symbolTicker,orderId=order_id)
        except:
            time.sleep(2)
            filled_order=client.get_order(symbol=symbolTicker,orderId=order_id)

        if filled_order['status'] =='FILLED':
            on = False
            order = {
                "order_id":filled_order["orderId"],
                "side":filled_order["side"],
                "origQty":filled_order["origQty"],
                "quantity":filled_order["executedQty"],
                "price":filled_order["price"],
                "total":str(float(filled_order["price"])*float(filled_order["executedQty"])),
                "symbolTicker":symbolTicker,
                "status":filled_order['status'],
                }   
            print(f'{Color.ROJO}>------>>COMPRO<<------<{Color.RESET}')
        else:
            # current_symbolPrice = get_indicator(symbolTicker)['close']
            try:
                current_symbolPrice = float(lastprice(symbolTicker))
            except:
                time.sleep(2)
                current_symbolPrice = float(lastprice(symbolTicker))
            print('--')
            print(f'    Prev Price = {Color.ROJO}{str(prev_symbolPrice)}{Color.RESET}')
            print(f'   Price Order = {Color.BLANCO}{str(float(round(prev_symbolPrice*stop_buy[1],info["minPrice"])))}{Color.RESET}')
            print(f' Current Price = {Color.VERDE}{str(current_symbolPrice)}{Color.RESET}')

            if ( prev_symbolPrice > current_symbolPrice):            
                result = client.cancel_order(
                    symbol = symbolTicker,
                    orderId = order_id
                )
                buyOrder = client.create_order(
                    symbol = symbolTicker,
                    side = 'BUY',
                    type = 'STOP_LOSS_LIMIT',
                    quantity = float(round(quan["quantityBuy"]/round(current_symbolPrice*stop_buy[1],2),info["minQty"])),
                    price = str(float(round(current_symbolPrice*stop_buy[0],info["minPrice"]))),
                    stopPrice = str(float(round(current_symbolPrice*stop_buy[1],info["minPrice"]))),
                    timeInForce = 'GTC'
                )
                print(f'{Color.AZUL}Orden Cambiada{Color.RESET}')
                telegram_bot(f'💲 Previo: {prev_symbolPrice} \n💲Orden: {float(round(prev_symbolPrice*stop_buy[1],info["minPrice"]))} \n💲Actual: {current_symbolPrice}')
                prev_symbolPrice = current_symbolPrice
    return   order

def dinamic_order_sell(symbolTicker,quan,stop_sell,orderId=0):
    order = {}
    # print(orderId,quan,stop_sell)

    # prev_symbolPrice = get_indicator(symbolTicker)['close']
    try:    
        prev_symbolPrice = float(lastprice(symbolTicker))
    except:
        time.sleep(2)    
        prev_symbolPrice = float(lastprice(symbolTicker))
    try:    
        info = symbol_info(symbolTicker)
    except:
        time.sleep(2)    
        info = symbol_info(symbolTicker)
    if orderId != 0:
        print(orderId)
        cancel_stop = client.cancel_order(
                        symbol = symbolTicker,
                        orderId = orderId
                    )
    sellOrder = client.create_order(
        symbol = symbolTicker,
        side = 'SELL',
        type = 'STOP_LOSS_LIMIT',
        quantity = float(round(quan["quantitySell"],info["minQty"])),
        price = str(float(round(prev_symbolPrice*stop_sell[0],info["minPrice"]))),
        stopPrice = str(float(round(prev_symbolPrice*stop_sell[1],info["minPrice"]))),
        timeInForce = 'GTC'
    )

    print(f'{Color.AZUL}!!====>Orden Creada<====!!{Color.RESET}') 
    telegram_bot(f'Start dinamic *SELL* order *{symbolTicker}* _{prev_symbolPrice}_')
    
    on = True
    while on == True:
        time.sleep(10)

        try:
            order_id = sellOrder.get('orderId')
        except:
            time.sleep(2)    
            order_id = sellOrder.get('orderId')
        try:    
            filled_order=client.get_order(symbol=symbolTicker,orderId=order_id)
        except:
            time.sleep(2)    
            filled_order=client.get_order(symbol=symbolTicker,orderId=order_id)

        if filled_order['status'] =='FILLED':
            on = False
            order = {
                "order_id":filled_order["orderId"],
                "side":filled_order["side"],
                "origQty":filled_order["origQty"],
                "quantity":filled_order["executedQty"],
                "price":filled_order["price"],
                "total":str(float(filled_order["price"])*float(filled_order["executedQty"])),
                "symbolTicker":symbolTicker,
                "status":filled_order['status'],
                }   
            print(f'{Color.ROJO}>------->>VENDIO<<------<{Color.RESET}')
        else:
            # current_symbolPrice = get_indicator(symbolTicker)['close']
            try:    
                current_symbolPrice = float(lastprice(symbolTicker))
            except:
                time.sleep(2)    
                current_symbolPrice = float(lastprice(symbolTicker))
            print('--')
            print(f'    Prev Price = {Color.ROJO}{str(prev_symbolPrice)}{Color.RESET}')
            print(f'   Price Order = {Color.BLANCO}{str(float(round(prev_symbolPrice*stop_sell[1],info["minPrice"])))}{Color.RESET}')     
            print(f' Current Price = {Color.VERDE}{str(current_symbolPrice)}{Color.RESET}')

            if ( prev_symbolPrice < current_symbolPrice):
                result = client.cancel_order(
                    symbol = symbolTicker,
                    orderId = order_id
                )
                sellOrder = client.create_order(
                    symbol = symbolTicker,
                    side = 'SELL',
                    type = 'STOP_LOSS_LIMIT',
                    quantity = float(round(quan["quantitySell"],info["minQty"])),
                    price = str(float(round(prev_symbolPrice*stop_sell[0],info["minPrice"]))),
                    stopPrice = str(float(round(prev_symbolPrice*stop_sell[1],info["minPrice"]))),
                    timeInForce = 'GTC'
                )           
                print(f'{Color.AZUL}Orden Cambiada{Color.RESET}')
                telegram_bot(f'💲 Previo: {prev_symbolPrice} \n💲Orden: {float(round(prev_symbolPrice*stop_sell[1],info["minPrice"]))} \n💲Actual: {current_symbolPrice}')
                prev_symbolPrice = current_symbolPrice
        
    return   order

def order_stop(symbolTicker,quan,valor_compra,porcent,orderId=0):
    order = {}
    # # prev_symbolPrice = get_indicator(symbolTicker)['close']
    try:    
        prev_symbolPrice = float(lastprice(symbolTicker))
    except:
        time.sleep(2)    
        prev_symbolPrice = float(lastprice(symbolTicker))
    try:    
        info = symbol_info(symbolTicker)
    except:
        time.sleep(2)
        info = symbol_info(symbolTicker)
    if orderId != 0:
        #print(orderId)
        cancel_stop = client.cancel_order(
                        symbol = symbolTicker,
                        orderId = orderId
                    )
    sellOrder = client.create_order(
        symbol = symbolTicker,
        side = 'SELL',
        type = 'STOP_LOSS_LIMIT',
        quantity = float(round(quan["quantitySell"],info["minQty"])),
        price = str(float(round(valor_compra*porcent[0],info["minPrice"]))),
        stopPrice = str(float(round(valor_compra*porcent[1],info["minPrice"]))),
        timeInForce = 'GTC'
    )

    print(f'{Color.AZUL}!!====>Orden Creada<====!!{Color.RESET}') 
    create_order = sellOrder.get('orderId')
    create_stop = client.get_order(symbol=symbolTicker,orderId=create_order)
# remplazar por create_stop
    order = {
        "order_id":create_stop["orderId"],
        "side":create_stop["side"],
        "origQty":create_stop["origQty"],
        "quantity":create_stop["origQty"],
        "price":create_stop["price"],
        "total":str(float(create_stop["price"])*float(create_stop["origQty"])),
        "symbolTicker":symbolTicker,
        "status":create_stop["status"],
        }        
    return   order
