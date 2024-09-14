# This project Contains following items
1. Django Channels for the Asynchronous communication
2. ASGI server to server the ASGI requests
3. Celery to schedule the task at 10 second of intervals to update the stock price
4. Stock Comparison page, to compare the stocks for different companies, which will be changing every 10 second using celery
5. Used Redis as a Broker