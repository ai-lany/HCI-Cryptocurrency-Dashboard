import requests
import json
APIURL = "https://api.coingecko.com/api/v3"
COINTOURL = {
    "Bitcoin":"/coins/bitcoin",
    "Ethereum":"/coins/ethereum",
    "Solana":"/coins/solana"
}
def getChartData(coin, numDays):
    response = requests.get(APIURL+COINTOURL.get(coin)+ "/market_chart?vs_currency=usd&days=" + numDays)
    data = response.text
    return json.loads(data)

print(getChartData("Solana", "1"))