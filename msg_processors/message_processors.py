import requests
import json
from settings import *
import logging

#todo: move these to a settings-esque file and state that they could come from DB
WEATHER_PATTERNS = ["what's the weather in <Location>",
                    "weather in <Location>",
                    "<Location> weather"]
logger = logging.getLogger('testlogger')


def process_message(request_post):
    if u'text' in request_post:
        # poss_addres = give_address_on_match(request_post[u'text'], WEATHER_PATTERNS)
        poss_addres = seek_like_patterns_from_list(request_post[u'text'], WEATHER_PATTERNS, '<Location>')
        if poss_addres:
            weather_curr = give_weather(poss_addres)
            if weather_curr:
                return "Currently its " + give_weather(poss_addres) + " in " + poss_addres
            else:
                # state this was an assumption
                return "We don't know what the weather is in " + poss_addres
        else:
            return "Sorry, what was that?"  # todo state assumption that we need to send SOMETHING


def give_address_on_match(text, pattern_ls):
    lower_word_ls = text.lower().split()
    original_text_ls = text.lower().split()

    for possible_pattern in pattern_ls:  # no enumerate?
        possible_pattern_ls = str.lower(possible_pattern).split()

        overlap_words = set(possible_pattern_ls).intersection(lower_word_ls)

        possible_pattern_ls.remove("<location>")
        if set(overlap_words) == set(possible_pattern_ls):
            for overlap_wd in overlap_words:
                lower_word_ls.remove(overlap_wd)
            address_text = lower_word_ls
            for address_wd in address_text:
                original_text_ls.remove(address_wd)
            non_address_text = original_text_ls
            if possible_pattern_ls == non_address_text:
                address_str = " ".join(address_text)
                if address_str in text.lower():
                    return address_str
            # todo state assumption that address service does not care about case
            # todo: MAYBE swap address for <location> and be sure its the same sentance


# todo: consider a form that might return more than one match?
def seek_like_patterns_from_list(text, pattern_ls, common_key):
    if not text or not pattern_ls or not common_key:
        logger.error("call to seek_like_patterns_from_list missing values " + str(seek_like_patterns_from_list) +
               "|" + str(pattern_ls) + "|" + str(common_key))
        return None
    for pattern in pattern_ls:
        poss_key_match = find_patterns_in_text(text, pattern, common_key)
        if poss_key_match:
            return poss_key_match


def find_patterns_in_text(text, pattern, pattern_key):
    pattern_ls = pattern.lower().split()
    pattern_key = pattern_key.lower()
    text_lower = text.lower()

    if pattern_key in pattern_ls:
        key_idx = pattern_ls.index(pattern_key)
        pre_match_txt = " ".join(pattern_ls[0:key_idx])
        post_match_txt = " ".join(pattern_ls[key_idx+1:len(pattern_ls)])

    else:
        logger.error(" No pattern " + pattern_key + " in " + pattern)
        return

    if (len(pre_match_txt) > 0 and pre_match_txt in text_lower) or \
            (len(post_match_txt) > 0 and post_match_txt in text_lower):

        # Be sure these arent partials
        if (len(pre_match_txt) > 0 and text_lower.index(pre_match_txt) != 0) or \
                (len(post_match_txt) > 0 and text_lower.index(post_match_txt) != len(text) - len(post_match_txt)):
            return
        return text[len(pre_match_txt):len(text_lower) - len(post_match_txt)].lstrip().rstrip()

    else:
        # this is not an error!
        return


def give_weather(address):
    location = get_coordinates(address)
    if location and 'lat' in location and 'lng' in location:
        weather_request = DARKSKY_FULL_API_KEY + str(location['lat']) + "," + str(location['lng'])
        response = requests.get(weather_request)
        if response and hasattr(response, 'json'):
            if 'currently' in response.json():
                if 'temperature' in response.json()['currently'] and 'summary' in response.json()['currently']:
                    return str(response.json()['currently']['temperature']) + 'F ' + \
                           str(response.json()['currently']['summary'])
        logger.error("Unexpected or empty return format in " + DARKSKY_FULL_API_KEY + "|" + str(response))
    logger.error("Unexpected or empty return format in get_coordinates " + str(location))


def get_coordinates(address):
    response = requests.post(GOOGLE_API_MAP_URL,
                      params={'address': address, 'key': GOOGLE_API_KEY})
    if response and hasattr(response, 'json'):
        response_text = response.json()
        if 'results' in response_text:
            for res in response_text['results']:
                if 'geometry' in res:
                    if 'location' in res['geometry']:
                        return res['geometry']['location']
    logger.error("Unexpected or empty return format in " + GOOGLE_API_MAP_URL + "|" + str(response))


if __name__ == '__main__':
    print str(give_address_on_match("Herman bob weather", WEATHER_PATTERNS))
    print str(give_address_on_match("what's the weather in large hamster", WEATHER_PATTERNS))
    print str(give_address_on_match("what's the weather in <Location>", WEATHER_PATTERNS))

    print str(give_address_on_match("weather what's the in large hamster fake address", WEATHER_PATTERNS))
    print str(give_address_on_match("What is the weather in blah blah ssuper niot", WEATHER_PATTERNS))

    print " ++++ "
    print str(seek_like_patterns_from_list("Herman bob weather", WEATHER_PATTERNS, "<Location>"))
    print str(seek_like_patterns_from_list("what's the weather in large hamster", WEATHER_PATTERNS, "<Location>"))
    print str(seek_like_patterns_from_list("what's the weather in <Location>", WEATHER_PATTERNS, "<Location>"))
    print str(seek_like_patterns_from_list("well, what's the weather in <Location>", WEATHER_PATTERNS, "<Location>"))

    print str(seek_like_patterns_from_list("weather the in large hamster fake address", WEATHER_PATTERNS, "<Location>"))
    print str(seek_like_patterns_from_list("What is the weather in blah blah super nice", WEATHER_PATTERNS, "<Location>"))



