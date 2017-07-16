from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def process_messages(request):
    print " >> RECEIVED: " + str(request.POST)

    data = {
        "messages": [
            {
                "type": "text",
                "text": "Sorry, I don't have any sandwiches, but have a picture instead:"
            },
            {
                "type": "rich",
                "html": "<img src='http://i.imgur.com/J9DLQ.png'>"
            }
        ]
    }

    return HttpResponse(json.dumps(data), content_type="application/json")
