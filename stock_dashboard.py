import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Dashboard Graph Function 
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

#Get Tesla Stock Information
tesla_ticker = yf.Ticker("TSLA")
tesla_stock_data = tesla_ticker.history(period="max")
tesla_stock_data.reset_index(inplace=True)
tesla_stock_data.head(5)

#Get and return request from macrotrend servers
tesla_url="https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
tesla_request = requests.get(tesla_url).text

#Parse with BS
tesla_revenue_data_parser = bs(tesla_request,"html.parser")
tesla_tables = tesla_revenue_data_parser.find_all("table")

#Loop through each table and fine quarterly earnings table and save index
for index, row in enumerate(tesla_tables):
    if("Quarterly" in str(row)):
        table_index = index

#Instantiate Tesla Revenune Dataframe
tesla_frame = pd.DataFrame(columns=["Date","Revenue"])

#Loop through the table and append date and revenue data to dataframe
for row in tesla_tables[table_index].tbody.find_all("tr"):
    cols = row.find_all("td")
    if(cols != []):
        date = cols[0].text
        revenue = cols[1].text
        tesla_frame = tesla_frame.append({"Date":date,"Revenue":revenue},ignore_index=True)

#Remove all non-int chars from revenue values
tesla_frame["Revenue"] = tesla_frame['Revenue'].str.replace(',|\$',"")

#Clean data by discarding all 'nan' values
tesla_frame.dropna(inplace=True)
tesla_frame = tesla_frame[tesla_frame['Revenue'] != ""]

#Get gamestock ticker info
gamestop_ticker = yf.Ticker("GME")
gamestop_stock_data = gamestop_ticker.history(period="max")
gamestop_stock_data.reset_index(inplace=True)
gamestop_stock_data.head(5)

#Get and return Gamestop revenue info via macrotrends
gamestop_url="https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue."
gamestop_request = requests.get(gamestop_url).text

#Parse with BS
gamestop_revenue_data_parser = bs(gamestop_request,"html.parser")
gamestop_tables = gamestop_revenue_data_parser.find_all("table")

#Loops through tables until finding quarterly earnings
for index,row in enumerate(gamestop_tables):
    if("Quarterly" in str(row)):
        table_index = index

#Instantiate Dataframe
gamestop_frame = pd.DataFrame(columns=["Date","Revenue"])

#Loop through table and append data/revenue data to dataframe
for row in gamestop_tables[table_index].tbody.find_all("tr"):
    cols = row.find_all("td")
    if(cols != []):
        date = cols[0].text
        revenue = cols[1].text
        gamestop_frame = gamestop_frame.append({"Date":date,"Revenue":revenue},ignore_index=True)

gamestop_frame["Revenue"] = gamestop_frame["Revenue"].str.replace(",|\$","")
gamestop_frame.head()

gamestop_frame.dropna(inplace=True)
gamestop_frame = gamestop_frame[gamestop_frame["Revenue"]!=""]

#Visualize Dataframes via dashboard
make_graph(tesla_stock_data,tesla_frame,"Tesla")
make_graph(gamestop_stock_data,gamestop_frame,"Game Stop")