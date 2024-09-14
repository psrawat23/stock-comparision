from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from threading import Thread
import pandas as pd
from yahoo_fin.stock_info import get_data
from channels.layers import get_channel_layer
import asyncio

def get_last_data(ticker):
    
    '''Gets the live price of input ticker
    
       @param: ticker
    '''    
    df = get_data(ticker, end_date = pd.Timestamp.today() + pd.DateOffset(10),interval = "1d")
    # Get the last record
    last_record = df.iloc[-1]  
    return last_record


def ReturnComparision(stock,data):
    details =get_last_data(stock)
    data.append(details.to_dict())


@shared_task(bind=True)
def update_stock(self,selected_stocks):
	data = []
	threads = []
	for stock in selected_stocks:
		threads.append(Thread(target=ReturnComparision,args=(stock,data)))
		threads[-1].start()
	
	for thread in threads:
		thread.join()
	
	# send data to group
	channel_layer = get_channel_layer()
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.run_until_complete(channel_layer.group_send("stock_track",
	{
		'type': 'send_stock_update',
		'message': data,
	}))