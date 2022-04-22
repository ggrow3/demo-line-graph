import streamlit as st
import pandas as pd
import altair as alt
from pandas_datareader import data


def get_stock_df(symbol, start, end):
    source = 'yahoo'
    df = data.DataReader(
        symbol, start=start, end=end, data_source=source
    )
    return df


def get_stock_combined(symbols, start, end):
    dfs = []
    for symbol in symbols.keys():
        df = get_stock_df(symbol, start, end)
        df['Symbol'] = symbol
        df['SymbolFullName'] = symbols[symbol]
        dfs.append(df)
    df_combined = pd.concat(dfs, axis=0)
    df_combined['date'] = df_combined.index.values
    return df_combined


def get_stock_title(stocks):
    title = ""
    idx = 0

    for i in stocks.keys():
        title = title + stocks[i]

        if idx < len(stocks.keys()) - 1:
            title = title + " & "
        idx = idx + 1

    return title


stocks = {"LIT": "Lithium", "USO": "United States Oil ETF",
          "UNG": "Natural Gas Fund", "USL": "US 12 Month Natural Gas Fund (UNL)"}
stock_title = get_stock_title(stocks)
start = '2021-06-01'
end = '2022-08-01'

df_combined = get_stock_combined(stocks, start, end)

line = alt.Chart(df_combined).mark_line().encode(
    alt.X("date", title="Date"),
    alt.Y("Close", title="Closing Price", scale=alt.Scale(zero=False)),
    color='SymbolFullName'
).properties(
    height=400, width=850,
    title=stock_title
).configure_title(
    fontSize=16
).configure_axis(
    titleFontSize=14,
    labelFontSize=12
)
line
