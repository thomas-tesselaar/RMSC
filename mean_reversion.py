
from market_access import *
import numpy as np
from time import sleep


def main():
    tick, status = get_tick()
    ticker_list = ['OWL', 'CROW', 'DOVE', 'DUCK']
    
    # Historical prices for moving average
    price_history = {ticker: [] for ticker in ticker_list}
    
    while status == 'ACTIVE':
        for ticker in ticker_list:
            best_bid_price, best_ask_price = get_bid_ask(ticker)
            last_price = get_last_price(ticker)
            position = get_position(ticker)
            
            if last_price is None or best_bid_price is None or best_ask_price is None:
                continue
            
            # Update price history and calculate moving average
            price_history[ticker].append(last_price)
            # if len(price_history[ticker]) > LOOKBACK_PERIOD:
            #     price_history[ticker].pop(0)
            
            # if len(price_history[ticker]) < LOOKBACK_PERIOD:
            #     continue
            
            moving_avg = np.mean(price_history[ticker])
            deviation = (last_price - moving_avg) / moving_avg
            
            # Mean reversion signals
            if deviation > DEVIATION_THRESHOLD and position > MAX_SHORT_EXPOSURE:
                # Price is above mean, sell
                place_order(ticker, 'SELL', best_bid_price, ORDER_LIMIT)
            elif deviation < -DEVIATION_THRESHOLD and position < MAX_LONG_EXPOSURE:
                # Price is below mean, buy
                place_order(ticker, 'BUY', best_ask_price, ORDER_LIMIT)
            
            sleep(0.75)  # Avoid API rate limits
        
        tick, status = get_tick()

if __name__ == '__main__':
    main()


