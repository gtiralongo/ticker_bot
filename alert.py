import config
import requests
import smtplib


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
