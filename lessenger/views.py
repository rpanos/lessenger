from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from msg_processors.msg_routers import route_post_request

import json


@csrf_exempt
def process_messages(request):
    print " >> RECEIVED: " + str(request.POST)

    response_text = route_post_request(request.POST)

    data = {
        "messages": [
            {
                "type": "text",
                "text": response_text
            }
        ]
    }

    return HttpResponse(json.dumps(data), content_type="application/json")
