# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async, async_to_sync
from django_celery_beat.models import PeriodicTask,  IntervalSchedule
class StockConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def addToCeleryBeat(self,stockpicker):
        task = PeriodicTask.objects.filter(name="every-10-seconds")
        if len(task) > 0:
            task = task.first()
            args = json.load(task.args)
            args = args[0]
            for x in stockpicker:
                if x not in args:
                    args.append(x)
            task.args = json.dumps([args])
            task.save()
        else:
            schedule, created  = IntervalSchedule.objects.get_or_create(every=10,period=IntervalSchedule.SECONDS)
            task  = PeriodicTask.objects.create(interval=schedule,name='every-10-seconds', task="front.tasks.update_stock",args=json.dumps([stockpicker]))
            


    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"stock_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, 
            self.channel_name
            )

        # parse queryString
        query_params = parse_qs(self.scope["query_string"].decode())
        stockpicker = query_params.get('stocks',[])

        # add to celery beat
        await self.addToCeleryBeat(stockpicker)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
              {"type": "stock_update",
                "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    async def stock_update(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))