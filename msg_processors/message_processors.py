import requests
from settings import *

#todo: move these to a settings-esque file and state that they could come from DB
WEATHER_PATTERNS = ["what's the weather in <Location>",
                    "weather in <Location>",
                    "<Location> weather"]


def process_message(request_post):
    if u'text' in request_post:
        poss_addres = give_address_on_match(request_post[u'text'], WEATHER_PATTERNS)
        if poss_addres:
            return give_weather(poss_addres)
            # todo consider throwing an error
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
                # print " CONFIRMED MATCH " + str(possible_pattern_ls) + "|" + str(non_address_text) + "\n"
                address_str = " ".join(address_text)
                if address_str in text.lower():
                    return address_str

            # todo state assumption that address service does not care about case
            # todo: MAYBE swap address for <location> and be sure its the same sentance


def seek_like_patterns_from_list(text, pattern_ls, common_key):

    for pattern in pattern_ls:
        poss_key_match = find_patterns_in_text(text, pattern, common_key)
        if poss_key_match:
            print "=====>> FOUND poss_key_match: " + poss_key_match


def find_patterns_in_text(text, pattern, pattern_key):
    # text_ls = text.lower().split()
    pattern_ls = pattern.lower().split()
    pattern_key = pattern_key.lower()
    text_lower = text.lower()
    print "pattern_ls: " + str(pattern_ls)

    if pattern_key in pattern_ls:
        key_idx = pattern_ls.index(pattern_key)
        print " key_idx " + str(key_idx)
    # else:
    # if key_idx > -1:
        pre_match_txt = " ".join(pattern_ls[0:key_idx])
        post_match_txt = " ".join(pattern_ls[key_idx+1:len(pattern_ls)])

    else:
        print " No pattern " + pattern_key + " in " + pattern
        # todo log error
        return

    # if (pre_match_txt in text or len(pre_match_txt) == 0) and \
    #     (post_match_txt in text or len(post_match_txt) == 0):
    # if (pre_match_txt in text or len(pre_match_txt) == 0) and \
    #     (post_match_txt in text or len(post_match_txt) == 0):

    print "SEEKING :" + pattern + "| in |" + text_lower

    if (len(pre_match_txt) > 0 and pre_match_txt in text_lower) or \
            (len(post_match_txt) > 0 and post_match_txt in text_lower):

        print ">> pre_match_txt: " + pre_match_txt
        print ">> post_match_txt: " + post_match_txt
        # Be sure these arent partials
        if (len(pre_match_txt) > 0 and text_lower.index(pre_match_txt) != 0) or \
            (len(post_match_txt) > 0 and text_lower.index(post_match_txt) != len(text) - len(post_match_txt)):
            print " Partials! "
            print str(text_lower.index(post_match_txt)) + " != " + str(len(text_lower) - len(post_match_txt))
            print " text_lower.index(pre_match_txt) " + str(text_lower.index(pre_match_txt))
            return
        key_match = text[len(pre_match_txt):len(text_lower) - len(post_match_txt)]
        print "=========================key_match: " + key_match
        return key_match
    else:
        # this is not an error!
        return




def give_weather(address):
    data = get_coordinates(address)
    return "Its Hot in " + address + "!"


def get_coordinates(address):
    response = requests.post(GOOGLE_API_MAP_URL,
                      params={'address': address, 'key': GOOGLE_API_KEY})
    print " >> geocode: " + str(response)

    if 'results' in response:
        print "response[results] " + str(response['results'])
    if hasattr(response, 'text'):
        print "response.text " + str(response.text)
    return response


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

    print str(seek_like_patterns_from_list("weather what's the in large hamster fake address", WEATHER_PATTERNS, "<Location>"))
    print str(seek_like_patterns_from_list("What is the weather in blah blah ssuper niot", WEATHER_PATTERNS, "<Location>"))



