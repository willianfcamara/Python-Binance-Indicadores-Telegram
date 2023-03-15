# Python-Binance-Indicadores-Telegram
Indicador tecnico binance que envia mensagem telegram

Este código é um bot para análise de criptomoedas que utiliza a API da Binance para obter dados de preços históricos e indicadores técnicos, e envia mensagens no Telegram quando há oportunidades de compra ou venda. O código utiliza as bibliotecas time, telegram, binance, pandas, ta, e asyncio.

O programa começa importando as bibliotecas necessárias e definindo as variáveis api_key e api_secret para se conectar à API da Binance. Em seguida, ele utiliza a biblioteca telegram para definir o token do bot que será utilizado para enviar as mensagens.

Depois disso, são definidos os pares de criptomoedas que serão analisados (symbols), bem como as configurações de take_profit_percent e stop_loss_percent.

A seguir, há duas funções principais. A primeira (get_historical_data) utiliza a função client.get_historical_klines da biblioteca binance para obter dados de preços históricos em um determinado intervalo de tempo (definido por interval e limit), e retorna um DataFrame do pandas com os dados relevantes. A segunda (calculate_indicators) utiliza a biblioteca ta para calcular os valores dos indicadores Keltner e RSI a partir dos dados do DataFrame retornado pela primeira função.

A terceira função (analyze_market) é responsável por analisar o mercado para um determinado par de criptomoedas. Ela utiliza o DataFrame retornado pela função get_historical_data e o DataFrame retornado pela função calculate_indicators para tomar a decisão de compra ou venda com base em uma estratégia específica (no caso deste código, se o preço atual estiver acima da banda superior de Keltner e o RSI estiver acima de 70, o bot deve vender; se o preço atual estiver abaixo da banda inferior de Keltner e o RSI estiver abaixo de 30, o bot deve comprar).

A função send_telegram_message é responsável por enviar as mensagens no Telegram. Ela utiliza a função bot.send_message da biblioteca telegram para enviar a mensagem com o texto message para o chat ID.

A função main é a função principal do programa. Ela utiliza um loop infinito para executar a análise de mercado para cada par de criptomoedas a cada 5 minutos, utilizando as funções analyze_market e send_telegram_message para tomar decisões e enviar mensagens. O loop principal é executado com a ajuda da biblioteca asyncio.

Por fim, a função asyncio.run(main()) é utilizada para iniciar a execução do programa.
