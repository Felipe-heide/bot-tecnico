import pandas as pd
import requests
import time
import funciones

def get_historical_prices():
    """
    Fetches the historical Bitcoin prices from CryptoCompare API.
    Returns a list of closing prices.
    """
    url = 'https://min-api.cryptocompare.com/data/v2/histominute?fsym=BTC&tsym=USD&limit=2000&aggregate=1'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching historical prices: {response.status_code}")
        return []

    data = response.json()
    price_data = data['Data']['Data']
    return [price['close'] for price in price_data]

def get_current_price():
    """
    Fetches the current Bitcoin price from CoinGecko API.
    Returns the current price or None if an error occurs.
    """
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        response.raise_for_status()
        return response.json()['bitcoin']['usd']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching current price: {e}")
        return None

def main():
    invested_amount = 0
    purchase_price = 0
    historical_prices = get_historical_prices()

    while True:
        current_price = get_current_price()
        if current_price is None:
            continue

        historical_prices.append(current_price)

        rsi_75 = funciones.rsi(historical_prices[-75:])
        macd = funciones.macd(historical_prices[-75:])
        mms = funciones.mms(historical_prices[-50:])
        support_level, resistance_level = funciones.Nivel_Soporte_Resistencia(historical_prices[-50:])

        print(f"CURRENT BTC: {current_price}")
        print("________________________________________________________________________________")
        print(f"RSI 75: {rsi_75}")
        print(f"MACD: {macd}")
        print(f"MMS: {mms}")
        print(f"Nivel_Soporte: {support_level}")
        print(f"Nivel_Resistencia: {resistance_level}")
        print("\n")

        # Evaluate RSI
        if rsi_75 < 40:
            rsi_75_es = "SuperPositivo"
        elif rsi_75 > 70:
            rsi_75_es = "SuperNegativo"
        elif rsi_75 - 40 > 70 - rsi_75:
            rsi_75_es = "Negativo"
        else:
            rsi_75_es = "Positivo"

        # Evaluate MACD
        macd_es = "Positivo" if macd > 0 else "Negativo"

        # Evaluate support and resistance levels
        nivel_es = "Positivo" if current_price - support_level > resistance_level - current_price else "Negativo"

        # Evaluate MMS
        mms_es = "Positivo" if mms < current_price else "Negativo"

        print("RSI: " + rsi_75_es)
        print("MACD: " + macd_es)
        print("MMS: " + mms_es)
        print("NIVEL: " + nivel_es)
        print("\n")

        if invested_amount != 0 and purchase_price != 0:
            print(f"Cantidad Invertida: {invested_amount}")
            print(f"Precio De Compra: {purchase_price}")
            profit_amount = invested_amount * ((current_price - purchase_price) / purchase_price)
            profit_percentage = (current_price - purchase_price) / purchase_price * 100
            print(f"Desde la compra hubo un aumento del: {profit_percentage:.2f}%")
            print(f"Ganaste: {profit_amount:.2f}")
            print(f"Ahora tienes: {invested_amount + profit_amount:.2f}")

        if purchase_price == 0:
            decision = input("Quieres invertir [S]i, [N]o: ").lower()
            if decision == "s":
                invested_amount = float(input("Cantidad: "))
                purchase_price = current_price
            else:
                print("No se invertirá")

        print("\n")
        time.sleep(60)

if __name__ == "__main__":
    main()
