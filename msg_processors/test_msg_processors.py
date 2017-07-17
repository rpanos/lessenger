from django.test import TestCase
from message_processors import give_address_on_match



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



