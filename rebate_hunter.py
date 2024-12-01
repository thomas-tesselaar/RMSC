# make active trades when there is a tight spread in order to collect the rebate

from market_access import *
from time import sleep

ORDER_SIZE = 1000

def main():
    # Define constants for the strategy
    SPREAD_THRESHOLD = {'DOVE':0.01}  # Spread threshold (absolute or percentage, depending on your choice)
    ticker_list = ['CROW', 'DOVE']  # Securities to trade
    
    tick, status = get_tick()

    while status == 'ACTIVE':
        for ticker in ticker_list:
            # Get the best bid and ask prices
            best_bid_price, best_ask_price = get_bid_ask(ticker)
            
            # Calculate the spread
            spread = best_ask_price - best_bid_price

            # Check if the spread is below the threshold
            if spread <= SPREAD_THRESHOLD[ticker]:
                # Place a BUY order at the best bid price
                place_order(ticker, 'BUY', ORDER_SIZE, 'MARKET')

                # Place a SELL order at the best ask price
                place_order(ticker, 'SELL', ORDER_SIZE, 'MARKET')
            
            # Sleep to avoid overwhelming the API
            sleep(0.01)

        # Update the tick and status for the next iteration
        tick, status = get_tick()

if __name__=='__main__':
    main()



