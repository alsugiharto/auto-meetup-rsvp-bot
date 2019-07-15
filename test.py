import unittest
import auto_meetup_rsvp_bot

# Test variables
GROUP_NAME_NO_EVENT = "mysqlnyc"
GROUP_NAME_MULTI_EVENTS = "Amsterdam-Language-Cafe"
GROUP_NAME_ONE_AVAILABLE = "Cloud-Native-Kubernetes-Amsterdam"
GROUP_NAME_ONE_CANNOT_GO = "Site-Reliability-Engineering-Amsterdam"
GROUP_NAME_ONE_ALREADY_RSVP = "Amsterdam-Futsal-5v5-Indoor-Football"
# difficult to find a group with cancelled upcoming event
GROUP_NAME_ONE_CANCELLED = ""


class TestSum(unittest.TestCase):

    def test_main_multi_event(self):
        auto_meetup_rsvp_bot.update_group_name(GROUP_NAME_MULTI_EVENTS)
        browser = auto_meetup_rsvp_bot.main_login_setup(False)
        test_result = auto_meetup_rsvp_bot.new_coming_event_count(browser)
        self.assertGreater(test_result, 1)

    def test_main_no_event(self):
        auto_meetup_rsvp_bot.update_group_name(GROUP_NAME_NO_EVENT)
        browser = auto_meetup_rsvp_bot.main_login_setup(False)
        test_result = auto_meetup_rsvp_bot.new_coming_event_count(browser)
        self.assertEqual(test_result, 0)

    def test_main_one_already_rsvp(self):
        auto_meetup_rsvp_bot.update_group_name(GROUP_NAME_ONE_ALREADY_RSVP)
        browser = auto_meetup_rsvp_bot.main_login_setup(False)
        test_result = auto_meetup_rsvp_bot.new_coming_event_count(browser)
        self.assertEqual(test_result, 1)
        test_result = auto_meetup_rsvp_bot.is_event_available(browser)
        self.assertEqual(test_result, 2)

    def test_main_one_cannot_go(self):
        auto_meetup_rsvp_bot.update_group_name(GROUP_NAME_ONE_CANNOT_GO)
        browser = auto_meetup_rsvp_bot.main_login_setup(False)
        test_result = auto_meetup_rsvp_bot.new_coming_event_count(browser)
        self.assertEqual(test_result, 1)
        test_result = auto_meetup_rsvp_bot.is_event_available(browser)
        self.assertEqual(test_result, 3)

    def test_main_one_available(self):
        auto_meetup_rsvp_bot.update_group_name(GROUP_NAME_ONE_AVAILABLE)
        browser = auto_meetup_rsvp_bot.main_login_setup(False)
        test_result = auto_meetup_rsvp_bot.new_coming_event_count(browser)
        self.assertEqual(test_result, 1)
        test_result = auto_meetup_rsvp_bot.is_event_available(browser)
        self.assertEqual(test_result, 4)


if __name__ == '__main__':
    unittest.main()
