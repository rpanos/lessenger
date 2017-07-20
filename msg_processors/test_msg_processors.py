from django.test import TestCase
from message_processors import give_address_on_match, seek_like_patterns_from_list



class MsgTestCase(TestCase):

    # Todo move to a settings-esque file
    WEATHER_PATTERNS = ["what's the weather in <Location>",
                    "weather in <Location>",
                    "<Location> weather"]

    # def setUp(self):
    #     print " did setup "


    def test_set_match(self):
        self.assertEqual(give_address_on_match("Herman bob weather", self.WEATHER_PATTERNS), "herman bob")
        self.assertEqual(give_address_on_match("what's the weather in large hamster", self.WEATHER_PATTERNS),
                         "large hamster")
        self.assertEqual(give_address_on_match("what's the weather in 1234 hamster", self.WEATHER_PATTERNS),
                         "1234 hamster")
        self.assertEqual(give_address_on_match("weather what's the in large hamster fake address",
                                               self.WEATHER_PATTERNS), None)
        self.assertEqual(give_address_on_match("what's the weather in blah blah ssuper niot",
                                               self.WEATHER_PATTERNS), "blah blah ssuper niot")

        self.assertEqual(seek_like_patterns_from_list("Herman bob weather", self.WEATHER_PATTERNS, "<Location>"),
                         "Herman bob")
        self.assertEqual(seek_like_patterns_from_list("what's the weather in large hamster", self.WEATHER_PATTERNS, "<Location>"),
                         "large hamster")
        self.assertEqual(seek_like_patterns_from_list("what's the weather in <Location>", self.WEATHER_PATTERNS, "<Location>"),
                         "<Location>")
        self.assertEqual(seek_like_patterns_from_list("well, what's the weather in <Location>", self.WEATHER_PATTERNS, "<Location>"),
                         None)
        self.assertEqual(seek_like_patterns_from_list("weather the in large hamster fake addres", self.WEATHER_PATTERNS, "<Location>"),
                         None)
        self.assertEqual(seek_like_patterns_from_list("What is the weather in blah blah super nice", self.WEATHER_PATTERNS, "<Location>"),
                         None)
