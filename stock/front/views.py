from django.shortcuts import render
from yahoo_fin.stock_info import get_data, get_stats, get_income_statement,get_live_price, tickers_nifty50, get_company_officers, get_quote_data, get_day_gainers, get_quote_table
# Create your views here.
from django.http import JsonResponse, Http404
import json
import pandas as pd
import requests
from io import StringIO
import pandas as pd
from front.forms import StockSelectionForm
from threading import Thread
import requests
def index(request):
    top_stocks = tickers_nifty50(include_company_data=True)
    # top_stocks = json.load(top_stocks)
    # print(top_stocks)
    # out = requests.get("https://kr95ien2dj.execute-api.us-east-1.amazonaws.com/dev")
    # print(out.text)
    data_dict = top_stocks.to_dict(orient='records')
    print(data_dict)
    return render(request,'front/home.html',{'top_stocks':data_dict})


def ReturnComparision(stock,data):
    details =get_last_data(stock)
    data.append(details.to_dict())


def CompareStocks(request):        
    all_stocks = tickers_nifty50()
    STOCK_CHOICES = [(stock,stock) for stock in all_stocks]

    form = StockSelectionForm(stock_choices=STOCK_CHOICES)
    
    return render(request,'front/compare_stocks.html',{'all_stocks':all_stocks,'form':form,'room_name':'track'})



def returnCompare(request):   
    all_stocks = tickers_nifty50()
    STOCK_CHOICES = [(stock,stock) for stock in all_stocks]
    if request.method == 'GET':
        form = StockSelectionForm(request.GET, stock_choices=STOCK_CHOICES)
        if form.is_valid():
            selected_stocks = form.cleaned_data.get('stocks')
            data = []
            threads = []
            for stock in selected_stocks:
                threads.append(Thread(target=ReturnComparision,args=(stock,data)))
                threads[-1].start()
            for thread in threads:
                thread.join()
            return render(request,'front/compare_stocks.html',{'all_stocks':all_stocks,'comparison':data,'form':form,'room_name':'track'})
        else:
            print("FORM IS NOT VALID")
            return Http404
    else:
        print("Method is POST")
        return Http404
    

def force_float(elt):
    
    try:
        return float(elt)
    except:
        return elt

def get_last_data(ticker):
    
    '''Gets the live price of input ticker
    
       @param: ticker
    '''    
    
    df = get_data(ticker, end_date = pd.Timestamp.today() + pd.DateOffset(10),interval = "1d")
    # Get the last record
    last_record = df.iloc[-1]
    
    return last_record

def StockDetail(request,stock):
    try:
        data = get_data(stock)
        data_dict = data.to_dict(orient='records')
        return render(request,'front/detail.html',{'stock_detail':data_dict})
    except Exception as e:
        return Http404