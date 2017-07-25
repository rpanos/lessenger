
from greetings import process_join
from message_processors import process_message

def route_post_request(request_post):
    response_text  = None
    if u'action' in request_post:
        if u'join' in request_post[u'action']:
            response_text = process_join(request_post)

        elif u'message' in request_post[u'action']:
            response_text = process_message(request_post)

    return response_text