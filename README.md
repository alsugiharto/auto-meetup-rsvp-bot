# auto-meetup-rsvp-bot

A simple console app for lazy people to RSVP an event in meetup.com built in Python and Selenium using Chrome

### Why

I recently joined a football meetup group, where they only accept the first 12 RSVP players.
The event is always full after 3 minutes the event posted. You need dedication and quick fingers to be top 12 players out of 870 members.
As a lazy person using this tool, for the first time, I successfully RSVPed in the second place of the list, right after the event host. Hooray!

### Why Selenium not API?

I heard there are a few limitations using meetup API.
One of them to be that you cannot use API to RSVP in an event with waiting list (limited members can join an event).
We don't have this problem using Selenium.

### What to Do

The main purpose has been served.
There are some other minor features I would like to add:
- send email or SMS for RSVP success
- more browsers options to use
- multiple events options
- save and load credentials feature
- scheduling
- quit feature
- fix cookies waiting problem
- apply OOP

# How to install dependencies

### install git
[how to install git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### install pip
[how to install pip](https://pip.pypa.io/en/stable/installing/)

### install python
I use 3.5. Other python versions might work too.
[how to install python](https://www.python.org/downloads/release/python-354)

### install Chrome Browser
[how to install Chrome](https://support.google.com/chrome/answer/95346?co=GENIE.Platform%3DDesktop&hl=en)

### install Selenium
For Mac OS X, I put it here
```shell
/usr/local/bin/
```
Make sure you choose the same version like your Chrome version
[how to install selenium](https://selenium-python.readthedocs.io/installation.html)

# How to set Credentials
Make a python file named credentials.py with the following content and save.
```shell
USER_NAME = 'your_email_address@gmail.com'
PASSWORD = 'your_password'
GROUP_NAME = 'Name-of-your-meetup-group-you-want-to-RSVP-to' # make sure your group target only has one event at a time.
CHECK_TIME_SECOND = 40 # how often you want the app checks if there is a new upcoming event
```


# Setup and Run
After all of the dependencies are installed and the credential file is ready, then install and run
```shell
git clone https://github.com/alsugiharto/auto-meetup-rsvp-bot.git
cd auto-meetup-rsvp-bot
python main.py
```

# How it works

When you use the app for the first time. 
The app will try to log in with the given credential and save the session in your machine for the next use.
In the next use, the app won't try to login anymore but instead using the previous working session. 
In case the session doesn't work, then it will simply try to login again.

The app will check the event list of the group you mention in credentials.py.
There are 4 possibilities:
- There is no event, then the app will keep checking each CHECK_TIME_SECOND time
- There are multiple events, unfortunately, multiple events to choose is not possible yet. This will stop the app. Make sure your group target only has one event at a time.
- There is one upcoming event, the RSVP process should be started here. You will receive a message when it is. This will stop the app.
- Any error appears. This will stop the app.


# How to Quit
I don't have this feature yet. Please just force exit the terminal for now.
