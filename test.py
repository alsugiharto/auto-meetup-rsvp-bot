import unittest
import auto_meetup_rsvp_bot

# Test variables
GROUP_NAME_NO_EVENT = ""
GROUP_NAME_MULTI_EVENTS = ""
GROUP_NAME_ONE_AVAILABLE = ""
GROUP_NAME_ONE_CANNOT_GO = ""
GROUP_NAME_ONE_ALREADY_RSVP = ""
# difficult to find a group with cancelled upcoming event
GROUP_NAME_ONE_CANCELLED = ""


class TestSum(unittest.TestCase):

    # login function test
    def test_login(self):
        # get browser
        browser = auto_meetup_rsvp_bot.setup()
        # test before login
        before_login = auto_meetup_rsvp_bot.is_logged_in(browser)
        self.assertEqual(before_login, False)
        # login
        auto_meetup_rsvp_bot.login(browser)
        # test after login
        after_login = auto_meetup_rsvp_bot.is_logged_in(browser)
        self.assertEqual(after_login, True)

    # is_event_available function test
    # and
    # new_coming_event_count function test
    def test_main_multi_event(self):
        # update group name
        auto_meetup_rsvp_bot.update_group_name(GROUP_NAME_MULTI_EVENTS)
        # get browser
        browser = auto_meetup_rsvp_bot.setup()
        # login
        auto_meetup_rsvp_bot.login(browser)
        # new_coming_event_count function test
        test_result = auto_meetup_rsvp_bot.new_coming_event_count(browser)
        self.assertGreater(test_result, 1)

    def test_main_no_event(self):
        # update group name
        auto_meetup_rsvp_bot.update_group_name(GROUP_NAME_NO_EVENT)
        # get browser
        browser = auto_meetup_rsvp_bot.setup()
        # login
        auto_meetup_rsvp_bot.login(browser)
        # new_coming_event_count function test
        test_result = auto_meetup_rsvp_bot.new_coming_event_count(browser)
        self.assertEqual(test_result, 0)

    def test_main_one_already_rsvp(self):
        # update group name
        auto_meetup_rsvp_bot.update_group_name(GROUP_NAME_ONE_ALREADY_RSVP)
        # get browsr
        browser = auto_meetup_rsvp_bot.setup()
        # login
        auto_meetup_rsvp_bot.login(browser)
        # new_coming_event_count function test
        test_result = auto_meetup_rsvp_bot.new_coming_event_count(browser)
        self.assertEqual(test_result, 1)
        # is_event_available function test
        test_result = auto_meetup_rsvp_bot.is_event_available(browser)
        self.assertEqual(test_result, 2)

    def test_main_one_cannot_go(self):
        # update group name
        auto_meetup_rsvp_bot.update_group_name(GROUP_NAME_ONE_CANNOT_GO)
        browser = auto_meetup_rsvp_bot.setup()
        auto_meetup_rsvp_bot.login(browser)
        # new_coming_event_count function test
        test_result = auto_meetup_rsvp_bot.new_coming_event_count(browser)
        self.assertEqual(test_result, 1)
        # is_event_available function test
        test_result = auto_meetup_rsvp_bot.is_event_available(browser)
        self.assertEqual(test_result, 3)

    def test_main_one_available(self):
        # update group name
        auto_meetup_rsvp_bot.update_group_name(GROUP_NAME_ONE_AVAILABLE)
        # get browser
        browser = auto_meetup_rsvp_bot.setup()
        # login
        auto_meetup_rsvp_bot.login(browser)
        # new_coming_event_count function test
        test_result = auto_meetup_rsvp_bot.new_coming_event_count(browser)
        self.assertEqual(test_result, 1)
        # is_event_available function test
        test_result = auto_meetup_rsvp_bot.is_event_available(browser)
        self.assertEqual(test_result, 4)

    # TODO: fix RSVP test (waiting problem)
    # rsvp function test
    # def test_rsvp(self):
    #     # update group name
    #     auto_meetup_rsvp_bot.update_group_name(GROUP_NAME_ONE_AVAILABLE)
    #     # get browser
    #     browser = auto_meetup_rsvp_bot.setup()
    #     # login
    #     auto_meetup_rsvp_bot.login(browser)
    #
    #     # before rsvp
    #     # new_coming_event_count function test
    #     test_result = auto_meetup_rsvp_bot.new_coming_event_count(browser)
    #     self.assertEqual(test_result, 1)
    #     # is_event_available function test
    #     test_result = auto_meetup_rsvp_bot.is_event_available(browser)
    #     self.assertEqual(test_result, 4)
    #
    #     # rsvp
    #     auto_meetup_rsvp_bot.rsvp(browser)
    #
    #     # after rsvp
    #     # is_event_available function test
    #     test_result = auto_meetup_rsvp_bot.is_event_available(browser)
    #     self.assertEqual(test_result, 2)


if __name__ == '__main__':
    unittest.main()
