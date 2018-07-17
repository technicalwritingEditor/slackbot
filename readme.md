# SLACK BOT (By enol826)
## Quickstart (How to test it?)
In order to test the app:
1. Connect to your Slack workspace
2. Get your User and Bot tokens from Slack
3. The bot will look for incoming requests from the chosen channel.
5. Config the bot parameters (all of them in the class constructor), but specially the time management one. In the the Utils class constructor:
    - self.day = 5 # Day (see the 'days' dictionary below)
    - self.hour = 23 # Hour
    - self.minute = 30 # Minute
    - self.sec = 0 # Second
- days = {0:'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
4. Run the 'main.py' file (and make sure you're connected to the Internet)

## Dependencies (Python modules)
- [requests](http://docs.python-requests.org/en/master/)

## How the app is connected to Slack
FOR TESTING PURPOSES:
- The Slack Web API has been used (there were other options. Ex: Events app)
- Oauth has not been implemented. That is, I have requested Slack for a 'user token' and a 'bot token'
 (which do not expire) instead of implementing the Oauth process in the app.

I have decided to use the Web API because it did not require setting up a web server. I just needed a
workspace token (both user and bot) while the Events API used the principle "Don't call us, we'll call you".
    
## Functional requirements and achievement
- The bot will start looking for people coming for lunch at an specific day and time every week.
    Ex: Fridays at 10:00am
    --> Regardless of the day the app is executed, it finds the time remaining for the next Friday and sleeps
    until that date is reached.
- Once the day and time is reached, the bot will ask "Who's coming for lunch" and start counting the people coming
    --> The bot will read the channel messages and in order to sort whether a message is requesting a place
    in a lunch group, a few 'key words' will be taken into account.
    Those words are defined in the 'Config section' (i.e. Bot class constructor)
- The bot will stop listening for requests after X time
    --> The time time is also define in the 'Config section' (i.e. Bot class constructor)
- As soon as the bot has stopped listening for requests, it will set up the groups (max 7 people) appointing a leader
- Afterwards, channel notifications are sent with the groups information

## Structure
The development has been done following the principles of object oriented programming (having into account that 
Python is much more flexible language. Ex: getters and setters vs direct access to properties)

#### 'main.py'
    class App
        - The core of the app
        - Responsible for sleeping times of the process.
        - Gives orders to the Bot itself
        
#### 'utils.py'
    class Bot
        - Responsible for the functionality of the application
        - Connects to the Slack API
        - Processes people coming for lunch
        - Sets groups
        - Sends notifications to the channel
    class Group
        - Abstraction of a 'group'
        - Holds members (including a 'leader')
    class Utils
        - Responsible for some functions that are not directly part of the Bot abstraction
        - Exs: Messages of lunch approval, random selection, time management...

## Future improvements
- Auth system: Here, I'm just using some given tokens of an specific user.
- Testing: Unit testing
- More abstraction: Improve the Bot class abstraction, so it could reuse for further developing
- Code: Improve code clearness



