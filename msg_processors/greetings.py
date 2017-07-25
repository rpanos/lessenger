
import logging
logger = logging.getLogger('main_logger')
def process_join(request_post):

    if u'name' in request_post:
        return "Hello, " + request_post[u'name'] + "!"
    logger.info('Name expected in greeting; sending generic')
    return "Hiya.  What can I do for you?"  # assumed we should respond somehow

