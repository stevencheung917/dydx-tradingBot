from func_connections import connect_dydx
from func_private import abort_all_positions
from func_public import construct_market_prices
from func_cointegration import store_cointegration_results
from func_entry_pairs import open_positions
from func_exit_pairs import manage_trade_exits
from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED, PLACE_TRADES,MANAGE_EXITS
from func_messaging import send_message
from datetime import datetime

if __name__=="__main__":
        send_message("Little orange bot started!")
        
        try:
                print("Connecting to dydx..")
                
                client=connect_dydx()
        except Exception as e:
                print("Error connecting to dydx",e)
                exit(1)
        
        if ABORT_ALL_POSITIONS:
                try:
                        print("Close all positions")
                        close_orders=abort_all_positions(client)
                except Exception as e:
                        print("Error closing out all positions",e)
                        exit(1)
                        
        # Find conintegrated pairs
        if FIND_COINTEGRATED:
                try:
                        print("Fetching market prices...")
                        df_market_prices=construct_market_prices(client)
                        
                except Exception as e:
                        print("Error fetching market prices",e)
                        exit(1)
                
                try:
                        print("Storing cointegrated pairs...")
                        
                        stores_result=store_cointegration_results(df_market_prices)
                        if stores_result !="saved":
                                print("Error saving conint pairs")
                                exit(1)
                except Exception as e:
                        print("Error saving conint pairs",e)
                        exit(1)
                        
        # Place trades for opening positions
        while True: 
                if MANAGE_EXITS:
                        try:
                                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                print(f"Managing exits...,{timestamp}")
                                manage_trade_exits(client)
                        except Exception as e:
                                print("Error managing exiting positions: ", e)
                                send_message(f"Error managing exiting positions {e}")
                                exit(1)
                        
                # Place trades for opening positions
                if PLACE_TRADES:
                        try:
                                print("Finding trading opportunities...")
                                open_positions(client)
                        except Exception as e:
                                print("Error trading pairs: ", e)
                                send_message(f"Error opening trades {e}")
                                exit(1)
        
                
    