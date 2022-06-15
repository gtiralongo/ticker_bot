from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup 
from colorama import *
from funcion import *
from orders import *
import datetime
import logging
import config
import time

init(autoreset=True)
logging.basicConfig(level=logging.INFO,format="%(asctime)s-%(name)s-%(levelname)s-%(message)s-")

logger = logging.getLogger()

user_id = [756153269]
graf = ['15m', '30m', '1h', '4h', '1d', '1w', '1M']

def start(update, context):
    full_name = getattr(update.message.from_user, "full_name", "")
    chat_id = update.effective_chat.id
    logger.info(f"{full_name} esta saludando. ID: {chat_id}")
    runOff = "/run off"
    runOn = "/run on"
    resumen = "/resumen"
    quick_buy = "/quick buy"
    quick_sell = "/quick sell"
    info = "/infobot"  
    keyboard_run = [KeyboardButton(runOff), KeyboardButton(runOn)]
    keyboard_quick = [KeyboardButton(quick_buy), KeyboardButton(quick_sell)]
    keyboard_resumen = [KeyboardButton(resumen),KeyboardButton(info)]
    buttons = [keyboard_resumen, keyboard_run, keyboard_quick]
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        disable_web_page_preview=False,
        protect_content=True,
        text=f"""Hola 👋 {full_name}! Soy un bot 🤖 de cryptomonedas!
    Si te interesa tener acceso a mis funciones contactate con mi administrador 📲
    """ ,reply_markup=ReplyKeyboardMarkup(buttons)
    )

start_handler = CommandHandler('start', start)

def run(update, context):
    full_name = getattr(update.message.from_user, "full_name", "")
    chat_id = update.effective_chat.id
    logger.info(f"{full_name} inicio al bot trader. ID: {chat_id}")
    if update.effective_chat.id in user_id:
        data = ' '.join(context.args)
        data = data.lower()
        sep_data = data.split(' ')
        print(sep_data[0])
        save_info({"run":sep_data[0]},'action.json')
        if sep_data[0] == 'on':
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                disable_web_page_preview=False,
                protect_content=True,
                text=f"{full_name}, el bot esta en ejecución 🤖",
                parse_mode='Markdown'
            )
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                disable_web_page_preview=False,
                protect_content=True,
                text=f"{full_name}, el bot esta apagado 🚫",
                parse_mode='Markdown'
            )


    else:
        logger.info(f"Pero no tiene acceso. ID: {chat_id}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            disable_web_page_preview=False,
            protect_content=True,
            text=f"{full_name}, no tiene acceso a esta función ⛔, solicitar al administrador 📲"
        )

handeler_run = CommandHandler('run', run)

def quick (update, context):
    full_name = getattr(update.message.from_user, "full_name", "")
    chat_id = update.effective_chat.id
    logger.info(f"{full_name} inicio al bot trader. ID: {chat_id}")
    if update.effective_chat.id in user_id:
        data = ' '.join(context.args)
        data = data.lower()
        sep_data = data.split(' ')
        print(sep_data[0])
        save_info({"quick_order":sep_data[0]},'action.json')
        if sep_data[0] == 'buy':
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                disable_web_page_preview=False,
                protect_content=True,
                text=f"{full_name}, comienzo por eso de compra rapida 🤖",
                parse_mode='Markdown'
            )
        elif sep_data[0] == 'sell':
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                disable_web_page_preview=False,
                protect_content=True,
                text=f"{full_name}, comienzo por eso de venta rapida 🤖",
                parse_mode='Markdown'
            )

        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                disable_web_page_preview=False,
                protect_content=True,
                text=f"{full_name}, la función orden rápida está apagada 🚫",
                parse_mode='Markdown'
            )


    else:
        logger.info(f"Pero no tiene acceso. ID: {chat_id}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            disable_web_page_preview=False,
            protect_content=True,
            text=f"{full_name}, no tiene acceso a esta función ⛔, solicitar al administrador 📲"
        )

handeler_quick = CommandHandler('quick', quick)

def static_bot(update, context):
    full_name = getattr(update.message.from_user, "full_name", "")
    chat_id = update.effective_chat.id
    logger.info(f"{full_name} guardo info static trade. ID: {chat_id}")
    if update.effective_chat.id in user_id:
        data = ' '.join(context.args)
        sep_data = data.split(' ')
        if sep_data[6] == 'false':
            bug = False
        elif sep_data[6] == 'true':
            bug = True
        save_info( {"symbolTicker" : sep_data[0].upper(),
        "state" : sep_data[1].upper(),
        "graf_temp" : sep_data[2].lower(),
        "quantity" : {"quantityBuy": float(sep_data[3]) ,"quantitySell": float(sep_data[4])},
        "valor_compra" : float(sep_data[5]),
        "bug" : bug,
        "stop" : sep_data[7].lower(),
        "porcent_up": float(sep_data[8])},'action.json')
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            disable_web_page_preview=False,
            protect_content=True,
            text=f"{full_name}, las condiciones fueron ingrsadas con exito 💰",
        )

    else:
        logger.info(f"Pero no tiene acceso. ID: {chat_id}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            disable_web_page_preview=False,
            protect_content=True,
            text=f"{full_name}, no tiene acceso a esta función ⛔, solicitar al administrador 📲"
        )

handeler_static_bot = CommandHandler('static', static_bot)

def state_static_bot(update, context):
    full_name = getattr(update.message.from_user, "full_name", "")
    chat_id = update.effective_chat.id
    logger.info(f"{full_name} consulto info static trade. ID: {chat_id}")
    if update.effective_chat.id in user_id:
        info_static = get_save_info('action.json')
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            disable_web_page_preview=False,
            protect_content=True,
            text=f"Run: {info_static['run']}\nSymbol: {info_static['symbolTicker']}\nEstado:{info_static['state']}\nGrafico: {info_static['graf_temp']}\nStable-Coin:{info_static['quantity']}\nValor Compra: {info_static['valor_compra']}\nBug: {info_static['bug']}\nTime: {info_static['time']}\nStop: {info_static['stop']}\nPorcent_up: {info_static['porcent_up']}\nQuick: {info_static['quick_order']}\n",
        )


    else:
        logger.info(f"Pero no tiene acceso. ID: {chat_id}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            disable_web_page_preview=False,
            protect_content=True,
            text=f"{full_name}, no tiene acceso a esta función ⛔, solicitar al administrador 📲"
        )

handeler_info_static_bot = CommandHandler('infobot', state_static_bot)

def resumen(update, context):
    full_name = getattr(update.message.from_user, "full_name", "")
    chat_id = update.effective_chat.id
    logger.info(f"{full_name} pidio un resumen del trade. ID: {chat_id}")
    if update.effective_chat.id in user_id:
        save_info( {"resumen":"on"},'action.json')
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            disable_web_page_preview=False,
            protect_content=True,
            text=f"Procesando resumen 📊",
        )


    else:
        logger.info(f"Pero no tiene acceso. ID: {chat_id}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            disable_web_page_preview=False,
            protect_content=True,
            text=f"{full_name}, no tiene acceso a esta función ⛔, solicitar al administrador 📲"
        )

handeler_resumen = CommandHandler('resumen', resumen)

if __name__ == "__main__":

    updater = Updater(token=config.BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(handeler_run)
    dispatcher.add_handler(handeler_quick)
    dispatcher.add_handler(handeler_static_bot)
    dispatcher.add_handler(handeler_info_static_bot)
    dispatcher.add_handler(handeler_resumen)
    updater.start_polling(timeout=500)

def main():
    info_action = get_save_info('action.json')
    symbolTicker = info_action['symbolTicker']
    state = info_action['state']
    graf_temp = info_action['graf_temp']
    quantity = info_action['quantity']
    valor_compra =  info_action['valor_compra']
    porcent_up = info_action['porcent_up']
    TIMER = [10,14,18,22]
    FLAG_H = 0
    info_graf_temp = info_temp_trade(graf_temp)
    temp_up = info_graf_temp['temp_up']
    porcent_gan = info_graf_temp['porcent_gan']
    stop_sell = info_graf_temp['stop_sell']
    stop_buy = info_graf_temp['stop_buy']
    porcent_gan = porcent_up

    try:
        info_price=symbol_info(symbolTicker)
    except Exception as e:
        time.sleep(2)
        info_price=symbol_info(symbolTicker)
    while get_save_info('action.json')['run'] == 'on':
        info_action = get_save_info('action.json')
        symbolTicker = info_action['symbolTicker']
        state = info_action['state']
        graf_temp = info_action['graf_temp']
        quantity = info_action['quantity']
        valor_compra =  info_action['valor_compra']
        porcent_up = info_action['porcent_up']
        quick = info_action['quick_order']
        save_info({"time":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")},'action.json')
        print("---------------------------------------")
        print(f'Estado: {Color.AZUL}{state}{Color.RESET}  Grafico: {Color.AZUL}{graf_temp}{Color.RESET}')
        print(f'{symbolTicker[-3:]}: {Color.VERDE}{quantity["quantityBuy"]}{Color.RESET}  {symbolTicker[:-3]}: {Color.VERDE}{quantity["quantitySell"]}{Color.RESET}')
        print(f'{Color.CYAN}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{Color.RESET} ')
        print("---------------------------------------")
# ------------------------------------------------------------------------------------------------------------
#                                         PROCESO DE COMPRA
# ------------------------------------------------------------------------------------------------------------
        if state == 'BUY':
            try:
                indicator = get_indicator_temp(symbolTicker,graf_temp)[symbolTicker]
            except Exception as e:
                time.sleep(2)
                indicator = get_indicator_temp(symbolTicker,graf_temp)[symbolTicker]
                print(f'Indicador de {symbolTicker} estado {state}, error corrigiendo  ')
            try:
                indicator_up = get_indicator_temp(symbolTicker,temp_up)[symbolTicker]
            except Exception as e:
                time.sleep(2)
                indicator_up = get_indicator_temp(symbolTicker,temp_up)[symbolTicker]
                print(f'Indicador de {symbolTicker} estado {state}, error corrigiendo  ')
            try:
                indicator_1h = get_indicator_temp(symbolTicker,'1h')[symbolTicker]
            except Exception as e:
                time.sleep(2)
                indicator_1h = get_indicator_temp(symbolTicker,'1h')[symbolTicker]
                print(f'Indicador de {symbolTicker} estado {state}, error corrigiendo  ')
                
            if info_action['resumen'] == 'on':
                try:
                    trend = get_trend(symbolTicker,graf_temp)['trend']
                except Exception as e:
                    time.sleep(2)
                    trend = get_trend(symbolTicker,graf_temp)['trend']
                    print(f'Trend de {symbolTicker} estado {state}, error corrigiendo  ')
                resumen = (f'🪙Precio {symbolTicker[:-3]}: *${indicator["close"]}* \n💵{symbolTicker[-3:]}: *{quantity["quantityBuy"]}* \n⚙ Estado: {state}  🕘Grafico: {graf_temp}  \n💹Tendencia: {trend}\n⏳{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')  
                telegram_bot(resumen)
                save_info({"resumen":"off"},'action.json')
            if quick == "buy":
                try:
                    order_buy = dinamic_order_buy(symbolTicker,quantity,stop_buy) #--- Orden de compra
                except Exception as e:
                    time.sleep(2)
                    print(f'Buy order de {symbolTicker} estado {state}, el programa se detuvo Error: _{e}_')
                    order_buy = dinamic_order_buy(symbolTicker,quantity,stop_buy) #--- Orden de compra 
                quantity["quantitySell"] = float(order_buy["quantity"])
                quantity["quantityBuy"] = 0
                state = 'SELL'
                valor_compra = float(order_buy["price"])
                save_info({"state" : state,
                            "quantity" : {"quantityBuy": 0.0 ,"quantitySell": quantity[["quantitySell"]]},
                            "resumen" : "on",
                            "quick_order":"off",
                            "valor_compra" : valor_compra},'action.json')
                telegram_bot(f'🌕Orden de compra *{order_buy["symbolTicker"]}*\n📉Operacion: _{order_buy["side"]}_\n📊Precio: *{order_buy["price"]}*\n🪙{order_buy["symbolTicker"][:-4]}: {order_buy["quantity"]}\n💵{symbolTicker[-4:]} : {order_buy["total"]}\n🔢Order ID : {order_buy["order_id"]}\n🪐Profit: *{round(valor_compra+(valor_compra*(porcent_gan/100)),info_price["minPrice"])}*')
                save_info(order_buy,"ordenes.json")
                save_info({"quick_order":"off"},'action.json')
            if indicator_up['close'] > indicator_up['SMA20']:# and indicator_up['RSI'] >= 50:
                if indicator['close'] > indicator_1h['EMA50'] and indicator_1h['EMA20'] > indicator_1h['EMA50']:
                    print(f'{Color.CYAN}Buscando estrategia de compra')
                    if indicator["EMA50"] >= indicator["EMA20"] and indicator["EMA20"] >= indicator["EMA10"]:
                        print(f'{Color.AZUL}ESTRATEGIA FULL DOWN{Color.RESET}')
                        if indicator["SMA5"] <= indicator['close']:
                            if indicator["MACD.macd"] < 0 and indicator["RSI"] < 45:
                                try:
                                    order_buy = dinamic_order_buy(symbolTicker,quantity,stop_buy) #--- Orden de compra
                                except Exception as e:
                                    time.sleep(2)
                                    print(f'Buy order de {symbolTicker} estado {state}, el programa se detuvo Error: _{e}_')
                                    order_buy = dinamic_order_buy(symbolTicker,quantity,stop_buy) #--- Orden de compra  
                                quantity["quantitySell"] = float(order_buy["quantity"])
                                quantity["quantityBuy"] = 0
                                state = 'SELL'
                                valor_compra = float(order_buy["price"])
                                save_info({"state" : state,
                                            "quantity" : {"quantityBuy": 0.0 ,"quantitySell": quantity[["quantitySell"]]},
                                            "resumen" : "on",
                                            "valor_compra" : valor_compra,},'action.json')
                                telegram_bot(f'🌕Orden de compra *{order_buy["symbolTicker"]}*\n📉Operacion: _{order_buy["side"]}_\n📊Precio: *{order_buy["price"]}*\n🪙{order_buy["symbolTicker"][:-4]}: {order_buy["quantity"]}\n💵{symbolTicker[-4:]} : {order_buy["total"]}\n🔢Order ID : {order_buy["order_id"]}\n🪐Profit: *{round(valor_compra+(valor_compra*(porcent_gan/100)),info_price["minPrice"])}*')

                                save_info(order_buy, "ordenes.json")
                elif indicator["EMA20"] >= indicator["close"] and indicator["EMA50"] <= indicator["close"] and indicator["EMA10"] >= indicator["EMA20"]:                
                    if indicator["MACD.macd"]-indicator["MACD.signal"] < 0 and indicator["MACD.macd"] < indicator["MACD.signal"]:
                        if indicator["RSI"]> 40 and indicator["RSI"] < 55:
                            if indicator["ADX"] >= 40:
                                try:
                                    order_buy = dinamic_order_buy(symbolTicker,quantity,stop_buy) #--- Orden de compra
                                except Exception as e:
                                    time.sleep(2)
                                    print(f'Buy order de {symbolTicker} estado {state}, el programa se detuvo Error: _{e}_')
                                    order_buy = dinamic_order_buy(symbolTicker,quantity,stop_buy) #--- Orden de compra 
                                quantity["quantitySell"] = float(order_buy["quantity"])
                                quantity["quantityBuy"] = 0
                                state = 'SELL'
                                valor_compra = float(order_buy["price"])
                                save_info({"state" : state,
                                            "quantity" : {"quantityBuy": 0.0 ,"quantitySell": quantity[["quantitySell"]]},
                                            "resumen" : "on",
                                            "valor_compra" : valor_compra,},'action.json')
                                telegram_bot(f'🌕Orden de compra *{order_buy["symbolTicker"]}*\n📉Operacion: _{order_buy["side"]}_\n📊Precio: *{order_buy["price"]}*\n🪙{order_buy["symbolTicker"][:-4]}: {order_buy["quantity"]}\n💵{symbolTicker[-4:]} : {order_buy["total"]}\n🔢Order ID : {order_buy["order_id"]}\n🪐Profit: *{round(valor_compra+(valor_compra*(porcent_gan/100)),info_price["minPrice"])}*')

                                save_info(order_buy,"ordenes.json")
            else:
                print(f'{Color.ROJO}====> Esperando condiciones de compra <====={Color.RESET}')
# ------------------------------------------------------------------------------------------------------------
#                                         PROCESO DE VENTA
# ------------------------------------------------------------------------------------------------------------
        elif state == 'SELL':
            if quick == "sell":
                try:
                    order_sell = dinamic_order_sell(symbolTicker,quantity,stop_sell)
                except Exception as e:
                    print(f'Sell order de {symbolTicker} estado {state}, el programa se detuvo Error: _{e}_')
                    time.sleep(2)
                    order_sell = dinamic_order_sell(symbolTicker,quantity,stop_sell)
                quantity["quantityBuy"] = round(float(order_sell["price"])*float(order_sell["quantity"]),2)
                quantity["quantitySell"] = 0
                state = 'BUY'
                telegram_bot(f'🚀Vendimos \n😎{order_sell["symbolTicker"][:-3]} 💪*{round(((float(order_sell["price"])-valor_compra)*100)/valor_compra,2)}%*\n🔢Order ID : {order_sell["order_id"]}\n📉Operacion: {order_sell["side"]}\n🪙{order_sell["symbolTicker"][:-3]}: {order_sell["quantity"]}\n💵{order_sell["symbolTicker"][-3:]} : {float(order_sell["total"])}\n📊Precio: {order_sell["price"]}')
                save_info(order_sell,'ordenes.json')
                save_info({"state" : state,
                            "quantity" : {"quantityBuy": quantity["quantityBuy"] ,"quantitySell": 0.0},
                            "resumen" : "on",
                            "quick_order":"off",
                            "valor_compra" : 0.0,},'action.json')
            try:
                price = float(lastprice(symbolTicker))
            except Exception as e:
                print(f'Price de {symbolTicker} estado {state}, el programa se detuvo Error: _{e}_')
                time.sleep(2)
                price = float(lastprice(symbolTicker))
            porcent = round(((price-valor_compra)*100)/valor_compra,2)
            if info_action['resumen'] == 'on':
                try:
                    trend = get_trend(symbolTicker,graf_temp)['trend']
                except Exception as e:
                    time.sleep(2)
                    trend = get_trend(symbolTicker,graf_temp)['trend']
                    print(f'Trend de {symbolTicker} estado {state}, error corrigiendo  ')
                resumen = (f'🪙{symbolTicker[:-3]}: *{quantity["quantitySell"]}*\n⚙ Estado: {state}  🕘Grafico: {graf_temp}  \n💹Tendencia: {trend}\n🧾Valor de compra: _${valor_compra}_\n💲Precio actual: ${price} Porcentaje: *{porcent}%*\n💰Profit: _{round(valor_compra+(valor_compra*(porcent_gan/100)),info_price["minPrice"])}_  Profit %: _{round(porcent_gan,2)}%_\n⏳{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')    
                telegram_bot(resumen)
                save_info({"resumen":"off"},'action.json')
            if price <= valor_compra:
                val_comp = f'{Color.ROJO}{valor_compra}'
            else:
                val_comp = f'{Color.VERDE}{valor_compra}'
            print('==================================')
            print(f'Valor de compra $:{val_comp}')
            print(f'Precio actual $: {Color.VERDE}{price} {Color.RESET} Porcentaje: {Color.CYAN}{porcent}%')
            print(f'Profit: {Color.CYAN}{round(valor_compra+(valor_compra*(porcent_gan/100)),info_price["minPrice"])} {Color.RESET} Profit %: {Color.CYAN}{round(porcent_gan,2)}%')
            print('==================================')
            if porcent > porcent_gan:
                try:
                    order_sell = dinamic_order_sell(symbolTicker,quantity,stop_sell)
                except Exception as e:
                    print(f'Sell order de {symbolTicker} estado {state}, el programa se detuvo Error: _{e}_')
                    time.sleep(2)
                    order_sell = dinamic_order_sell(symbolTicker,quantity,stop_sell)
                quantity["quantityBuy"] = round(float(order_sell["price"])*float(order_sell["quantity"]),2)
                quantity["quantitySell"] = 0
                state = 'BUY'
                save_info({"state" : state,
                            "quantity" : {"quantityBuy": quantity["quantityBuy"] ,"quantitySell": 0.0},
                            "resumen" : "on",
                            "valor_compra" : 0.0,},'action.json')
                telegram_bot(f'🚀Vendimos \n😎{order_sell["symbolTicker"][:-3]} 💪*{round(((float(order_sell["price"])-valor_compra)*100)/valor_compra,2)}%*\n🔢Order ID : {order_sell["order_id"]}\n📉Operacion: {order_sell["side"]}\n🪙{order_sell["symbolTicker"][:-3]}: {order_sell["quantity"]}\n💵{order_sell["symbolTicker"][-3:]} : {float(order_sell["total"])}\n📊Precio: {order_sell["price"]}')
                save_info(order_sell,'ordenes.json')

            else:
                print(f'Precio debajo del valor de compra {valor_compra}') 
        for i in TIMER:
            if datetime.datetime.now().hour == i and datetime.datetime.now().minute == 00 and FLAG_H != i:
                try:
                    trend = get_trend(symbolTicker,graf_temp)['trend']
                except Exception as e:
                    time.sleep(2)
                    trend = get_trend(symbolTicker,graf_temp)['trend']
                    print(f'Trend de {symbolTicker} estado {state}, error corrigiendo  ')
                if state == 'SELL':
                    resumen = (f'🪙{symbolTicker[:-3]}: *{quantity["quantitySell"]}*\n⚙ Estado: {state}  🕘Grafico: {graf_temp}  \n💹Tendencia: {trend}\n🧾Valor de compra: _${valor_compra}_\n💲Precio actual: ${price} Porcentaje: *{porcent}%*\n💰Profit: _{round(valor_compra+(valor_compra*(porcent_gan/100)),info_price["minPrice"])}_  Profit %: _{round(porcent_gan,2)}%_\n⏳{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                elif state == 'BUY':
                    resumen = (f'🪙Precio {symbolTicker[:-3]}: *${indicator["close"]}* \n💵{symbolTicker[-3:]}: *{quantity["quantityBuy"]}* \n⚙ Estado: {state}  🕘Grafico: {graf_temp}  \n💹Tendencia: {trend}\n⏳{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')  
                telegram_bot(resumen)
                FLAG_H = i           
        time.sleep(5)
        info_action = get_save_info('action.json')['run']

while True:
    info_action = get_save_info('action.json')
    time.sleep(5)
    if info_action['run'] == 'on':
        main()
        print('Bot off')
