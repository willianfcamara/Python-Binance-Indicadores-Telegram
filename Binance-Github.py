import time
import telegram
from binance.client import Client
import pandas as pd
import ta
import asyncio

api_key = 'SUA API'
api_secret = 'SUA KEY'
client = Client(api_key, api_secret)

bot = telegram.Bot(token='TOKEN TELEGRAM')#LINHA 68 MODIFICAR COM O ID DO CHAT
#LINHA 68 MODIFICAR COM O ID DO CHAT

# Definir os pares de criptomoedas que você deseja analisar
symbols = ['SOLUSDT', 'ICXUSDT', 'STORJUSDT', 'BLZUSDT', 'UNIUSDT', 'AVAXUSDT']


# Configurações de Take Profit e Stop Loss
take_profit_percent = 5
stop_loss_percent = 5

# Obter dados históricos de preços
def get_historical_data(symbol, interval, limit):
    bars = client.get_historical_klines(symbol, interval, f"{limit} hours ago UTC")
    df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    df = df.set_index('date')
    df = df[['open', 'high', 'low', 'close', 'volume']]
    df = df.astype(float)
    return df

# Calcular os valores do indicador Keltner e do RSI
def calculate_indicators(df):
    keltner = ta.volatility.KeltnerChannel(df['high'], df['low'], df['close'], window=20, window_atr=2.5)
    rsi = ta.momentum.RSIIndicator(df['close'], window=14)
    df['keltner_upper_band'] = keltner.keltner_channel_hband()
    df['keltner_lower_band'] = keltner.keltner_channel_lband()
    df['rsi'] = rsi.rsi()
    return df

# Analisar o mercado e decidir se deve ser realizada uma compra ou venda
def analyze_market(symbol, interval, limit):
    df = get_historical_data(symbol, interval, limit)
    df = calculate_indicators(df)
    last_close = df['close'][-1]
    last_rsi = df['rsi'][-1]
    last_keltner_upper_band = df['keltner_upper_band'][-1]
    last_keltner_lower_band = df['keltner_lower_band'][-1]

    if last_close > last_keltner_upper_band and last_rsi > 70:
        decision = f'🔴 SELL - RSI ({last_rsi:.2f}) acima do limiar de venda (80)'
        target_price = last_close * (1 - take_profit_percent/100)
        stop_loss_price = last_close * (1 + stop_loss_percent/100)
        message = f"{decision}\nTake Profit: {target_price:.2f}\nStop Loss: {stop_loss_price:.2f}"
        return message
    elif last_close < last_keltner_lower_band and last_rsi < 30:
        decision = f'🟢 BUY - RSI ({last_rsi:.2f}) abaixo do limiar de compra (20)'
        target_price = last_close * (1 + take_profit_percent/100)
        stop_loss_price = last_close * (1 - stop_loss_percent/100)
        message = f"{decision}\nTake Profit: {target_price:.2f}\nStop Loss: {stop_loss_price:.2f}"
        return message
    else:
        return None

# Função para enviar mensagem no Telegram
async def send_telegram_message(message):
    await bot.send_message(chat_id='CHAT ID', text=message) 
    
# Loop para executar a análise de mercado a cada 5 minutos e enviar mensagens no Telegram quando houver oportunidade de compra ou venda
async def main():
    while True:
        for symbol in symbols:
            decision = analyze_market(symbol, Client.KLINE_INTERVAL_15MINUTE, 24)
            if decision is not None:
                timestamp = pd.Timestamp.now()
                hora = timestamp.strftime('%H:%M:%S')
                ticker = client.get_symbol_ticker(symbol=symbol)
                price = ticker['price']
                
                # Calculate take profit and stop loss prices
                target_price = float(price) * 1.05
                stop_loss_price = float(price) * 0.95
                
                message = f"\n⏰{hora} \n🏦{symbol} \n{decision} \n💲{price}" # \nTake Profit: {target_price:.2f} \nStop Loss: {stop_loss_price:.2f}"
                await send_telegram_message(message)
                
        # Fechar a conexão com a Binance
        client.close_connection()
        
        await asyncio.sleep(300)

# Executar o loop principal do programa
asyncio.run(main())
