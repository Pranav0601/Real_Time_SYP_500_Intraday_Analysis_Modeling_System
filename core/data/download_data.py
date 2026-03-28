import yfinance as yf
import pandas as pd
import os

def download_spy_data():
    symbol = "spy"  #spy etf tracks S&P 500

    #download 1-minute data for the last 7 days
    df = yf.download(
        symbol,
        interval="1m",
        period="7d",
    )

    #move datetime index to a column
    df.reset_index(inplace=True)

    df.columns = ["_".join(col).lower() if isinstance(col, tuple) else col.lower() for col in df.columns]#every column name in lowercase
    df.rename( columns = {
        "datetime_" : "timestamp"
    }, inplace = True)

    os.makedirs("data", exist_ok = True) #create data directory if it doesn't exist

    df.to_csv("data/spy_1m.csv") #save to csv

    print("Data downloaded and saved")
    print(df.head())

if __name__ == "__main__":
    download_spy_data()
