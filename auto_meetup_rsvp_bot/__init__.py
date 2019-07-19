import time
import datetime
import logging
import json
import random
# for error tracing
import traceback
# to save and load cookies
import pickle
# to use relative path
import os.path

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


MAIN_PATH = os.path.abspath(os.path.dirname(__file__))
LINK_LOGIN = 'https://secure.meetup.com/login/'
# add group name
LINK_EVENT_LIST = 'https://www.meetup.com/{}/events/'
# add group name and event id
LINK_EVENT_ONE = 'https://www.meetup.com/{}/events/{}/'
# add group name and event id
LINK_ATTENDEES_LIST = 'https://www.meetup.com/{}/events/{}/attendees'
# add group name and user account id
LINK_USER_PROFILE_HREF = '/{}/members/{}/profile/'
APP_NAME = 'meetupAutoRSVP'
COOKIES_FILE_NAME = 'cookies.pkl'
ERROR_HTML_PRINT_FILE_NAME = 'page_source.html'
# TODO: fix cookies problem  (waiting problem)
CONFIG_COOKIES = False
CONFIG_MESSAGES = True
CONFIG_LOGGING = True
CONFIG_HIDE_PROCESS = True
CONFIG_HIDE_IMAGES = True
CONFIG_TIME_WAIT_SELENIUM_SECOND = 10
CONFIG_CHECK_TIME_SECOND = 60
DELAY_RSVP_TIME_JSON = os.path.join(MAIN_PATH, 'data/delay_rsvp_time.json')
USER_ACCOUNT_JSON = os.path.join(MAIN_PATH, 'data/user_account.json')
USER_GROUP_JSON = os.path.join(MAIN_PATH, 'data/group_list.json')
USER_ACCOUNT = ''
GROUP_LIST = ''

with open(DELAY_RSVP_TIME_JSON) as json_data_second:
    DELAY_RSVP_TIME_JSON = random.choice(json.load(json_data_second))

with open(USER_ACCOUNT_JSON) as json_data_account:
    USER_ACCOUNT = json.load(json_data_account)

# ========================================
# CONSTANT UPDATING FUNCTION
# ========================================


# either manually set the group name for testing or from json file for real
def update_group_name(new_name=''):
    global GROUP_LIST

    if new_name is '':
        with open(USER_GROUP_JSON) as json_data_group:
            GROUP_LIST = json.load(json_data_group)
    else:
        data = list()
        data.append(new_name)
        GROUP_LIST = data


# return the updated link to event list with group name in it
def get_link_event_list():
    return LINK_EVENT_LIST.format(GROUP_LIST[0])


# return the updated link to event one with group name and event id in it
def get_link_event_one(event_id):
    return LINK_EVENT_ONE.format(GROUP_LIST[0], event_id)


# return the updated link to event one with group name and event id in it
def get_link_attendees_list(event_id):
    return LINK_ATTENDEES_LIST.format(GROUP_LIST[0], event_id)


# return the updated link to user profile with group name and user account id in it
def get_link_user_profile_href():
    return LINK_USER_PROFILE_HREF.format(GROUP_LIST[0], USER_ACCOUNT['ACCOUNT_ID'])

# ========================================
# SETUP AND INIT FUNCTION
# ========================================


# setting up and init of logging and selenium
def setup():
    # logging setup
    logging.basicConfig(filename='{}.log'.format(APP_NAME), level=logging.DEBUG, format='%(asctime)s %(message)s')

    # selenium setup to not open chrome windows
    chrome_options = Options()
    if CONFIG_HIDE_PROCESS:
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")

    if CONFIG_HIDE_IMAGES:
        sub_options = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'javascript': 2,
                                                            'plugins': 2, 'popups': 2, 'geolocation': 2,
                                                            'notifications': 2, 'auto_select_certificate': 2,
                                                            'fullscreen': 2,
                                                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                                            'media_stream_mic': 2, 'media_stream_camera': 2,
                                                            'protocol_handlers': 2,
                                                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                                            'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                            'metro_switch_to_desktop': 2,
                                                            'protected_media_identifier': 2, 'app_banner': 2,
                                                            'site_engagement': 2,
                                                            'durable_storage': 2}}
        chrome_options.add_experimental_option('prefs', sub_options)
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-extensions")

    # selenium INIT
    browser = webdriver.Chrome(options=chrome_options)
    # wait 10 seconds before each loading to make sure the page well loaded
    browser.implicitly_wait(CONFIG_TIME_WAIT_SELENIUM_SECOND)
    return browser

# ========================================
# LOG AND MESSAGE FUNCTION
# ========================================


# console message and logging
def alert_message(message, is_error=False):
    time_now = datetime.datetime.now()
    message = "CUSTOM MESSAGE {}".format(str(message))
    if is_error is True:
        # add traceback for debugging if error
        message = "{} {}".format(message, traceback.format_exc())
        if CONFIG_LOGGING:
            logging.error(message)
    else:
        if CONFIG_LOGGING:
            logging.info(message)
    if CONFIG_MESSAGES:
        print("{}: {}".format(time_now, message))


# save the HTML error page
def save_error_page(browser):
    with open(ERROR_HTML_PRINT_FILE_NAME, "w", encoding="utf-8") as f:
        f.write(browser.page_source)

# ========================================
# COOKIES FUNCTION
# ========================================


# login using old cookie, no need to re login
def cookies_load(browser):
    browser.get(LINK_LOGIN)
    try:
        for cookie in pickle.load(open(COOKIES_FILE_NAME, "rb")):
            browser.add_cookie({k: cookie[k] for k in ('name', 'value', 'domain', 'path') if k in cookie})
    except FileNotFoundError:
        alert_message('No cookies yet')
    return True


# save cookies for next use
def cookies_save(browser):
    browser.get(get_link_event_list())
    pickle.dump(browser.get_cookies(), open(COOKIES_FILE_NAME, "wb"))

# ========================================
# SELENIUM FUNCTION
# ========================================


# login using old cookie, no need to re login
def login(browser):
    browser.get(LINK_LOGIN)
    elem = browser.find_element_by_css_selector("#email")
    elem.send_keys(USER_ACCOUNT['USER_NAME'])
    elem = browser.find_element_by_css_selector("#password")
    elem.send_keys(USER_ACCOUNT['PASSWORD'])
    elem.send_keys(Keys.RETURN)


def is_logged_in(browser):
    return len(browser.find_elements_by_css_selector('#globalNav.authenticated')) > 0


# check if there are one upcoming event
def new_coming_event_count(browser):
    browser.get(get_link_event_list())
    return len(browser.find_elements_by_css_selector('.list-item'))


# check if the event available (not cancelled)
def is_event_available(browser):
    browser.get(get_link_event_list())
    if len(browser.find_elements_by_css_selector('.eventTimeDisplay.text--strikethrough')) > 0:
        # event is cancelled
        available_code = 1
    elif len(browser.find_elements_by_css_selector('.eventRsvpIndicator.eventRsvpIndicator--yes')) > 0:
        # event has been booked already
        available_code = 2
    elif len(browser.find_elements_by_css_selector('.eventRsvpIndicator.eventRsvpIndicator--no')) > 0:
        # event has been booked already and cancelled (cannot go)
        available_code = 3
    else:
        # available
        available_code = 4

    return available_code


# get event_id
def rsvp_get_event_id(browser):
    browser.get(get_link_event_list())
    event_button = browser.find_element_by_css_selector('.eventList-list .eventCardHead--title')
    event_link = event_button.get_attribute("href")
    event_id = os.path.split(os.path.dirname(event_link))[1]
    return event_id


# check rsvp status True for RSVP
def is_rsvp_check(browser):
    event_id = rsvp_get_event_id(browser)
    # go to attendees page
    attendees_link = get_link_attendees_list(event_id)
    browser.get(attendees_link)
    # check if user profile exists, yes means RSVP
    profile_link = get_link_user_profile_href()
    is_rsvp_return = len(browser.find_elements_by_css_selector('[href="{}"]'.format(profile_link))) > 0
    return is_rsvp_return


# go to the event link, click RSVP and check if RSVP works
def rsvp(browser):
    # get
    event_id = rsvp_get_event_id(browser)

    # waiting before RSVP, so that it's not too quick, avoid people wonder
    alert_message('Delay, we are going to book in {} seconds'.format(DELAY_RSVP_TIME_JSON))
    time.sleep(DELAY_RSVP_TIME_JSON)

    # click RSVP
    browser.get(get_link_event_one(event_id))
    browser.find_element_by_css_selector('.rsvpIndicator-button').click()

    # check if RSVP by checking if user profile exists in attendees list
    is_rsvp = is_rsvp_check(browser)

    # show which event has been booked
    alert_message('event link: {}'.format(get_link_event_one(event_id)))

    return is_rsvp


# exit all
def close_everything(browser):
    alert_message("Exit.")
    browser.close()
    exit()


# ========================================
# INTERACTION FUNCTION
# ========================================


# setting up the browser and login, decide to use cookies or new login
def main_login_setup(cookies=True):
    # setting up and init of logging and selenium
    browser = setup()

    if cookies:
        # login using old cookie, no need to re login
        cookies_load(browser)

    # check is the cookie working, otherwise login
    if is_logged_in(browser):
        alert_message("Cookies work, no login needed.")
    else:
        # login
        alert_message("Logging in.")
        login(browser)

    if cookies:
        # save cookies for next use
        cookies_save(browser)

    return browser


def main():
    # setting up the browser and login, decide to use cookies or new login
    browser = main_login_setup(CONFIG_COOKIES)

    alert_message("Start checking {} every {} seconds".format(GROUP_LIST[0], CONFIG_CHECK_TIME_SECOND))
    count_try = 0
    # looping each time to check
    while True:
        try:
            # counter
            count_try += 1

            # check if there are one upcoming event
            list_event_count = new_coming_event_count(browser)

            # if there is no event
            if list_event_count < 1:
                alert_message('{} No event is found. Keep waiting!'.format(count_try))

            # if there are multiple events to choose
            elif list_event_count > 1:
                alert_message('There are {} events. System only works for one event in group'.format(list_event_count))
                # exit all
                close_everything(browser)

            # if correct, there is one upcoming event
            else:
                alert_message('One event is available!')

                # check if the event available (not cancelled)
                is_available = is_event_available(browser)

                if is_available is 1:
                    alert_message('But it has been cancelled.')

                elif is_available is 2:
                    alert_message('But you already RSVP.')

                elif is_available is 3:
                    alert_message('But you already RSVP and cancel it (cannot go).')

                else:
                    # go to the event link, click RSVP and check if RSVP works
                    is_rsvp_success = rsvp(browser)

                    if is_rsvp_success:
                        alert_message('Congrats! You got the RSVP!')
                    else:
                        alert_message('Sorry, RSVP is failed', True)

                # exit all
                close_everything(browser)

            # sleep before re action
            time.sleep(CONFIG_CHECK_TIME_SECOND)

        # exit
        except KeyboardInterrupt:
            # exit all
            close_everything(browser)

        # other unknown error
        except Exception as e:
            alert_message("{}".format(e), True)
            # save the HTML error page
            save_error_page(browser)
            # exit all
            close_everything(browser)


if __name__ == '__main__':
    # update group here because for testing the group name is edited for each test
    update_group_name()
    # run the rest
    main()
