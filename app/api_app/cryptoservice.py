import cryptocompare

cryptocompare.cryptocompare._set_api_key_parameter('24b0b1c73aa9e5a995c51d76ebad08bd0e352d235ed9bacf56184d7a2cfb8296')

#Gibt den aktuellen Wert der Kryptowährung/en zurück
#Übergabeparameter ist ein Array von Strings mit den Abkürzungen der
#Kryptowährung. Bitcoin = 'BTC'
def getCurrentCryptoPrice(cryptocurrency):
    currentCryptoPrice = cryptocompare.get_price(cryptocurrency)
    return currentCryptoPrice

#Gibt die historischen Werte einer Kryptowährung zurück
#Übergabeparameter ist das Kürzel der Kryptowährung, Kürzel Währung und Datum
#date = datetime.datetime(2017,6,6)
def getHistoricalCryptoData(cryptocurrency, currency, date):
    historicalCryptoData = cryptocompare.get_historical_price(cryptocurrency, currency, date)
    return historicalCryptoData

def getAll():
    data = cryptocompare.get_coin_list(format=False)
    return data