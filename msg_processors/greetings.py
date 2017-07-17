

def process_join(request_post):

    if u'name' in request_post:
        return "Hello, " + request_post[u'name'] + "!"
    #todo consider throwing an error

