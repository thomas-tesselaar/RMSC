
from market_access import *
import numpy as np
from time import sleep

ORDER_SIZE = 1000
LOOKBACK_PERIOD = 20

def main():
    tick, status = get_tick()
    ticker_list = ['OWL', 'CROW', 'DOVE', 'DUCK']
    
    # Historical prices for moving average
    price_history = {ticker: [] for ticker in ticker_list}
    
    while status == 'ACTIVE':
        for ticker in ticker_list:
            # cancel any existing orders
            place_cancel(ticker)

            best_bid_price, best_ask_price = get_bid_ask(ticker)
            last_price = get_last_price(ticker)
            position = get_position(ticker)
            gross = get_gross_position()
            
            if last_price is None or best_bid_price is None or best_ask_price is None:
                continue
            
            # Update price history and calculate moving average
            price_history[ticker].append(last_price)
            if len(price_history[ticker]) > LOOKBACK_PERIOD:
                price_history[ticker].pop(0)
            
            if len(price_history[ticker]) < LOOKBACK_PERIOD:
                continue

            if tick<240:
                pass#sleep(0.1)
            
            moving_avg = np.mean(price_history[ticker])
            deviation = (last_price - moving_avg) / moving_avg
            if position>8000 and deviation < 0: deviation /= 2
            if position<8000 and deviation > 0: deviation /= 2

            # Mean reversion signals
            if deviation < -0.005 and position > MAX_SHORT_EXPOSURE+ORDER_SIZE+60000:
                if position < 0 and gross>GROSS_LIMIT-ORDER_SIZE:
                    continue
                # Price is above mean, sell
                print(f"placing sell order for {ticker}")
                place_order(ticker, 'SELL', best_bid_price, ORDER_SIZE)
            elif deviation > 0.005 and position < MAX_LONG_EXPOSURE-ORDER_SIZE-60000:
                if position > 0 and gross>GROSS_LIMIT-ORDER_SIZE:
                    continue
                # Price is below mean, buy
                print(f"placing buy order for {ticker}")
                place_order(ticker, 'BUY', best_ask_price, ORDER_SIZE)
            
            sleep(0.1)  # Avoid API rate limits
        
        tick, status = get_tick()

        


if __name__ == '__main__':
    main()