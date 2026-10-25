import pandas as pd

def route_demand(df):
    return df.groupby("route", as_index=False)["passengers"].sum().sort_values("passengers", ascending=False)

def hourly_demand(df):
    return df.groupby("hour", as_index=False)["passengers"].sum().sort_values("hour")
