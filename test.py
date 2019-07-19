import unittest
import time
import auto_meetup_rsvp_bot

# Test variables
# You need to find several meetup groups with the following criteria
GROUP_NAME_NO_EVENT = ""
GROUP_NAME_MULTI_EVENTS = ""
GROUP_NAME_ONE_AVAILABLE = ""
GROUP_NAME_ONE_CANNOT_GO = ""
GROUP_NAME_ONE_ALREADY_RSVP = ""
# difficult to find a group with cancelled upcoming event
GROUP_NAME_ONE_CANCELLED = ""


class TestSum(unittest.TestCase):

    # login function test
    def test01_login(self):
        # get browser
        browser = auto_meetup_rsvp_bot.setup()
        # login
        auto_meetup_rsvp_bot.login(browser)
        # test after login
        after_login = auto_meetup_rsvp_bot.is_logged_in(browser)
        self.assertEqual(after_login, True)

    # new_coming_event_count function test
    def test02_count_no_event(self):
        # update group name
        auto_meetup_rsvp_bot.update_group_name(GROUP_NAME_NO_EVENT)
        # get browser
        browser = auto_meetup_rsvp_bot.setup()
        # login
        auto_meetup_rsvp_bot.login(browser)
        # new_coming_event_count function test
        test_result = auto_meetup_rsvp_bot.new_coming_event_count(browser)
        self.assertEqual(test_result, 0)

    def test03_count_multi_event(self):
        # update group name
        auto_meetup_rsvp_bot.update_group_name(GROUP_NAME_MULTI_EVENTS)
        # get browser
        browser = auto_meetup_rsvp_bot.setup()
        # login
        auto_meetup_rsvp_bot.login(browser)
        # new_coming_event_count function test
        test_result = auto_meetup_rsvp_bot.new_coming_event_count(browser)
        self.assertGreater(test_result, 1)

    def test04_count_one_already_rsvp(self):
        # update group name
        auto_meetup_rsvp_bot.update_group_name(GROUP_NAME_ONE_ALREADY_RSVP)
        # get browsr
        browser = auto_meetup_rsvp_bot.setup()
        # login
        auto_meetup_rsvp_bot.login(browser)
        # new_coming_event_count function test
        test_result = auto_meetup_rsvp_bot.new_coming_event_count(browser)
        self.assertEqual(test_result, 1)

    def test05_count_one_available(self):
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
    def test06_available_one_already_rsvp(self):
        # update group name
        auto_meetup_rsvp_bot.update_group_name(GROUP_NAME_ONE_ALREADY_RSVP)
        # get browsr
        browser = auto_meetup_rsvp_bot.setup()
        # login
        auto_meetup_rsvp_bot.login(browser)
        # is_event_available function test
        test_result = auto_meetup_rsvp_bot.is_event_available(browser)
        self.assertEqual(test_result, 2)

    def test07_available_one_cannot_go(self):
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

    def test08_available_one_available(self):
        # update group name
        auto_meetup_rsvp_bot.update_group_name(GROUP_NAME_ONE_AVAILABLE)
        # get browser
        browser = auto_meetup_rsvp_bot.setup()
        # login
        auto_meetup_rsvp_bot.login(browser)
        # is_event_available function test
        test_result = auto_meetup_rsvp_bot.is_event_available(browser)
        self.assertEqual(test_result, 4)

    # RSVP function test
    def test09_rsvp_is_rsvp_check_yes(self):
        # update group name
        auto_meetup_rsvp_bot.update_group_name(GROUP_NAME_ONE_ALREADY_RSVP)
        # get browser
        browser = auto_meetup_rsvp_bot.setup()
        # login
        auto_meetup_rsvp_bot.login(browser)
        # is rsvp check yes test
        test_result = auto_meetup_rsvp_bot.is_rsvp_check(browser)
        self.assertEqual(test_result, True)

    def test10_rsvp_is_rsvp_check_no(self):
        # update group name
        auto_meetup_rsvp_bot.update_group_name(GROUP_NAME_ONE_AVAILABLE)
        # get browser
        browser = auto_meetup_rsvp_bot.setup()
        # login
        auto_meetup_rsvp_bot.login(browser)
        # is rsvp check no test
        test_result = auto_meetup_rsvp_bot.is_rsvp_check(browser)
        self.assertEqual(test_result, False)

    # WILL ACTUALLY RSVP!
    def test11_rsvp_final(self):
        # update group name
        auto_meetup_rsvp_bot.update_group_name(GROUP_NAME_ONE_AVAILABLE)
        # get browser
        browser = auto_meetup_rsvp_bot.setup()
        # login
        auto_meetup_rsvp_bot.login(browser)

        # delay
        time.sleep(10)

        # rsvp
        auto_meetup_rsvp_bot.rsvp(browser)

        # delay
        time.sleep(10)

        # after rsvp
        # is rsvp check yes test
        test_result = auto_meetup_rsvp_bot.is_rsvp_check(browser)
        self.assertEqual(test_result, True)


if __name__ == '__main__':
    unittest.main()
