
from greetings import process_join

def route_post_request(request_post):

    if u'action' in request_post:
        if u'join' in request_post[u'action']:
            response_text = process_join(request_post)



    return response_text