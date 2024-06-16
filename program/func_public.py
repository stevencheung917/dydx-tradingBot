from constants import RESOLUTION,NO_OF_MARKETS
from func_utils import get_ISO_times
import pandas as pd
import numpy as np
import time

from pprint import pprint

ISO_TIMES = get_ISO_times()


# Get Candles recent
def get_candles_recent(client, market):

    # Define output
    close_prices = []

    # Protect API
    time.sleep(0.2)

    # Get data
    candles = client.public.get_candles(
        market= market,
        resolution=RESOLUTION,
        limit=100
    )

    # Structure data
    for candle in candles.data["candles"]:
        close_prices.append(candle["close"])

    # Construct and return close price series
    close_prices.reverse()
    prices_result = np.array(close_prices).astype(np.float)
    return prices_result


def get_candles_historical(client,market):
    #Define output
    close_prices=[]

    for timeframe in ISO_TIMES.keys():
        tf_obj = ISO_TIMES[timeframe]
        from_iso =tf_obj['from_iso']
        to_iso =tf_obj['to_iso']
        
        time.sleep(0.2)
        
        candles=client.public.get_candles(
            market=market,
            resolution=RESOLUTION,
            from_iso=from_iso,
            to_iso=to_iso,
            limit=100
        )
        
        for candle in candles.data["candles"]:
            close_prices.append({"datetime":candle["startedAt"],market:candle["close"]})
    
    #construct and return dataframe
    close_prices.reverse()
    return close_prices

def construct_market_prices(client):
    #declare variables
    tradeable_markets=[]
    markets =client.public.get_markets()
    
    #find tradeable pairs
    for market in markets.data["markets"].keys():
        market_info=markets.data["markets"][market]
        if market_info["status"]=="ONLINE" and market_info["type"]=="PERPETUAL":
            tradeable_markets.append(market)
        
    #set initial dataframe
    close_prices = get_candles_historical(client,tradeable_markets[0])
    
    df =pd.DataFrame(close_prices)
    df.set_index("datetime",inplace=True)
    
    
    #append other prices to Dataframe
    i=0
    for market in tradeable_markets[1:NO_OF_MARKETS]:
        close_prices_add=get_candles_historical(client,market)
        time.sleep(1)
        df_add=pd.DataFrame(close_prices_add) 
        df_add.set_index("datetime",inplace=True)
        df=pd.merge(df,df_add,how="outer",on="datetime",copy=False)
        i=i+1
        print("remaining markets",len(tradeable_markets)-i)     
        del df_add
        
    #check any columns with NaNs
    nans=df.columns[df.isna().any()].tolist()
    if len(nans) >0:
        print("dropping columns:")
        print(nans)
        df.drop(columns=nans,inplace=True)
        
    #print(df.head(5))
    return df           