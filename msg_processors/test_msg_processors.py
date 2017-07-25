from django.test import TestCase
from message_processors import seek_like_patterns_from_list



class MsgTestCase(TestCase):

    # Todo move to a settings-esque file
    WEATHER_PATTERNS = ["what's the weather in <Location>",
                    "weather in <Location>",
                    "<Location> weather"]

    def test_set_match(self):
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
        self.assertEqual(seek_like_patterns_from_list("weather", self.WEATHER_PATTERNS, "<Location>"),
                         None)
        self.assertEqual(seek_like_patterns_from_list("", self.WEATHER_PATTERNS, "<Location>"),
                         None)
        self.assertEqual(seek_like_patterns_from_list(None, self.WEATHER_PATTERNS, "<Location>"),
                         None)
        self.assertEqual(seek_like_patterns_from_list(None, self.WEATHER_PATTERNS, None),
                         None)