import requests

s = requests.Session()
s.headers.update({'X-API-key': 'F5RK3J0F'}) # Make sure you use YOUR API Key

# global variables
MAX_LONG_EXPOSURE = 100000
MAX_SHORT_EXPOSURE = -100000
GROSS_LIMIT = 240000
ORDER_LIMIT = 5000
LOOKBACK_PERIOD = 20  # Moving average lookback period (ticks)
# DEVIATION_THRESHOLD = 0.02  # Threshold for mean reversion signal (2%)
DEVIATION_THRESHOLD = {'OWL':0.03,'CROW':0.045,'DOVE':0.06,'DUCK':0.045}

# SERVER = "http://flserver.rotman.utoronto.ca:10005" 
SERVER = "http://localhost:10001"


def get_tick():
    resp = s.get(f'{SERVER}/v1/case')
    if resp.ok:
        case = resp.json()
        return case['tick'], case['status']


def get_bid_ask(ticker):
    payload = {'ticker': ticker}
    resp = s.get (f'{SERVER}/v1/securities/book', params = payload)
    if resp.ok:
        book = resp.json()
        
        bid_prices_book = [item["price"] for item in book['bids']]
        ask_prices_book = [item['price'] for item in book['asks']]
        
        best_bid_price = bid_prices_book[0]
        best_ask_price = ask_prices_book[0]
  
        return best_bid_price, best_ask_price

def get_time_sales(ticker):
    payload = {'ticker': ticker}
    resp = s.get (f'{SERVER}/v1/securities/tas', params = payload)
    if resp.ok:
        book = resp.json()
        time_sales_book = [item["quantity"] for item in book]
        return time_sales_book
    
def get_last_price(ticker):
    payload = {'ticker': ticker}
    resp = s.get(f'{SERVER}/v1/securities/tas', params=payload)
    if resp.ok:
        trades = resp.json()
        return trades[0]['price'] if trades else None
    return None

def get_position(ticker):
    payload = {'ticker': ticker}
    resp = s.get (f'{SERVER}/v1/securities', params=payload)
    if resp.ok:
        book = resp.json()
        for b in book:
            if b['ticker'] == ticker:
                return b['position']

def get_gross_position():
    resp = s.get (f'{SERVER}/v1/securities')
    if resp.ok:
        book = resp.json()
        gross = 0
        for b in book:
            gross += abs(b['position'])
        return gross

def get_open_orders(ticker):
    payload = {'ticker': ticker}
    resp = s.get (f'{SERVER}/v1/orders', params = payload)
    if resp.ok:
        orders = resp.json()
        buy_orders = [item for item in orders if item["action"] == "BUY"]
        sell_orders = [item for item in orders if item["action"] == "SELL"]
        return buy_orders, sell_orders

def get_order_status(order_id):
    resp = s.get (f'{SERVER}/v1/orders' + '/' + str(order_id))
    if resp.ok:
        order = resp.json()
        return order['status']
    
def place_order(ticker, action, price, quantity, type='LIMIT'):
    params = {
        'ticker': ticker,
        'type': type,
        'quantity': quantity,
        'price': price,
        'action': action
    }
    resp = s.post(f'{SERVER}/v1/orders', params=params)
    return resp.ok

def place_cancel(ticker):
    payload = {'ticker': ticker}
    s.post (f'{SERVER}/v1/commands/cancel', params = payload)
