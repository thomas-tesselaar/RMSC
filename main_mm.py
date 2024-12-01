
from market_access import *
import numpy as np
from time import sleep

ORDER_SIZE = 5000
ORDER_SIZE2 = 2000

def main():
    tick, status = get_tick()
    ticker_list = ['OWL','CROW','DOVE','DUCK']
    target_spreads_tight = {'OWL':0.60,'CROW':0.70,'DOVE':0.20,'DUCK':0.30}
    target_spreads = {'OWL':1.50,'CROW':1.50,'DOVE':0.60,'DUCK':0.80}

    # Historical prices for moving average
    price_history = {ticker: [] for ticker in ticker_list}

    while status == 'ACTIVE':        

        for i in range(4):
            ticker = ticker_list[i]

            place_cancel(ticker)

            position = get_position(ticker)
            gross = get_gross_position()

            last_price = get_last_price(ticker)
            price_history[ticker].append(last_price)
            moving_avg = np.mean(price_history[ticker])
            deviation = (last_price - moving_avg) / moving_avg

            best_bid_price, best_ask_price = get_bid_ask(ticker)
            mid_price = (best_bid_price+best_ask_price)/2

            # account for mid price being off
            half_spread = (best_ask_price-best_bid_price)/2
            offset = 0.005* (int(100*half_spread + 0.0001)//2 == 1)
            tgt = target_spreads[ticker]/2
            tgt2 = target_spreads_tight[ticker]/2
       
            if position < MAX_LONG_EXPOSURE-ORDER_SIZE-70000:
                if position > 0 and gross>GROSS_LIMIT-ORDER_SIZE:
                    continue
                x = 0.08 if position < -5000 else 0
                x2 = 0.5 if position > 5000 else 1
                if ticker == 'OWL': x2*=0.25
                y = 0#int(100*min(deviation,0.04))/100
                place_order(ticker, 'BUY', mid_price-tgt-offset+x-y, ORDER_SIZE*x2)
                place_order(ticker, 'BUY', mid_price-tgt2-offset+x-y, ORDER_SIZE2*x2*x2)
                
            if position > MAX_SHORT_EXPOSURE+ORDER_SIZE+70000:
                if position < 0 and gross>GROSS_LIMIT-ORDER_SIZE:
                    continue
                x = 0.08 if position > 5000 else 0
                x2 = 0.5 if position < -5000 else 1
                if ticker == 'OWL': x2*=0.25
                y = 0#int(100*min(deviation,0.04))/100
                place_order(ticker, 'SELL', mid_price+tgt+offset-x-y, ORDER_SIZE*x2)
                place_order(ticker, 'SELL', mid_price+tgt2+offset-x-y, ORDER_SIZE2*x2*x2)

            sleep(0.1) 



        tick, status = get_tick()

if __name__ == '__main__':
    main()