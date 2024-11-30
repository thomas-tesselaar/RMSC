# make active trades when there is a tight spread in order to collect the rebate


def main():
    # Define constants for the strategy
    SPREAD_THRESHOLD = 0.02  # Spread threshold (absolute or percentage, depending on your choice)
    TICK_SLEEP_TIME = 0.5    # Delay between iterations (to avoid API rate limits)
    ticker_list = ['OWL', 'CROW', 'DOVE', 'DUCK']  # Securities to trade
    
    tick, status = get_tick()

    while status == 'ACTIVE':
        for ticker in ticker_list:
            # Get the best bid and ask prices
            best_bid_price, best_ask_price = get_bid_ask(ticker)

            if best_bid_price is None or best_ask_price is None:
                continue  # Skip this ticker if no data is available
            
            # Calculate the spread
            spread = best_ask_price - best_bid_price

            # Check if the spread is below the threshold
            if spread <= SPREAD_THRESHOLD:
                # Place a BUY order at the best bid price
                place_order(ticker, 'BUY', best_bid_price, ORDER_LIMIT)

                # Place a SELL order at the best ask price
                place_order(ticker, 'SELL', best_ask_price, ORDER_LIMIT)
            
            # Sleep to avoid overwhelming the API
            sleep(TICK_SLEEP_TIME)

        # Update the tick and status for the next iteration
        tick, status = get_tick()





