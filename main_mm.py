
from market_access import *
from time import sleep



def main():
    tick, status = get_tick()
    ticker_list = ['OWL','CROW','DOVE','DUCK']
    target_spreads = {}

    while status == 'ACTIVE':        

        for i in range(4):
            
            ticker_symbol = ticker_list[i]
            position = get_position()
            best_bid_price, best_ask_price = get_bid_ask(ticker_symbol)
       
            if position < MAX_LONG_EXPOSURE:
                resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': ticker_symbol, 'type': 'LIMIT', 'quantity': ORDER_LIMIT, 'price': best_bid_price, 'action': 'BUY'})
                
            if position > MAX_SHORT_EXPOSURE:
                resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': ticker_symbol, 'type': 'LIMIT', 'quantity': ORDER_LIMIT, 'price': best_ask_price, 'action': 'SELL'})

            sleep(0.75) 

            s.post('http://localhost:9999/v1/commands/cancel', params = {'ticker': ticker_symbol})

        tick, status = get_tick()

if __name__ == '__main__':
    main()