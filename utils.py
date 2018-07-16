import datetime
import time
import requests
import json
import math
import random
import threading

class Bot:

    # -------------- CONFIG (not to use in production) -------------- #
    def __init__(self):
        # We already have the tokens needed. Otherwise, Oauth must be implemented
        self.user_token = 'USER_TOKEN'
        self.bot_token = 'BOT_TOKEN'

        # Test channel in our workspace
        self.channel = 'CHANNEL_ID' # Channel ID
        self.slack_url = 'https://slack.com/api/'
        self.methods = {'chat.post':'chat.postMessage', 'chat.list':'conversations.history', 'user.info':'users.info'}

        # Arranging groups
        self.people = []
        self.groups = []
        self.max_people = 7 # Max number of people in a group
        self.time_requests = 10  # Time (in seconds) for a channel to be rechecked

        self.Utils = Utils()

    # -------------- API -------------- #
    def postMessage(self, message):
        requests.post(self.slack_url + self.methods['chat.post'],
                      {'token': self.bot_token, 'channel': self.channel,
                       'text': message})

    def readChannel(self,from_time):
        s = requests.get(self.slack_url + self.methods['chat.list'],{'token':self.user_token,'channel':self.channel,'oldest':from_time}).content
        return json.loads(s)

    def getUserInfo(self,user_id):
        s = requests.get(self.slack_url + self.methods['user.info'],{'token':self.bot_token,'user':user_id}).content
        return json.loads(s)

    # -------------- Bot tasks -------------- #
    # How much time does the bot process has to sleep until the next lunch day?
    def findNextDay(self):
        return self.Utils.nextDay()

    def start(self):
        Utils.log('1. Asking')
        self.postMessage('Who is coming for lunch today?')

    # We start the process of finding people coming for lunch
    def findPeople(self):
        Utils.log('2. Listening for requests')
        t = self.Utils.currentTimestamp()
        c = t + self.time_requests
        while t < c:
            s = self.readChannel(t) # Reading the channel
            for message in s['messages']: # Processing messages
                if 'user' in message:
                    user = self.getUserInfo(message['user'])['user']['name']
                    if (user not in self.people) and (self.Utils.wantsToCome(message['text']) == True):
                        self.people.append(user)
            t = self.Utils.currentTimestamp()
            threading._sleep(5)  # We check the conversation every 5 seconds
        Utils.log('--> People found: {0}', len(self.people))

    # Once requests are "close", we arrange groups
    def arrangeGroups(self):
        Utils.log('3. Arranging groups...')
        self.createGroups(len(self.people))
        Utils.log('--> Number of groups created: {0}', len(self.groups))
        for group in self.groups:
            while group.currentNumMembers() < group.numMembers():
                group.addMember(self.people.pop(self.Utils.selectRandomPeople(len(self.people))))
            group.printMembers()

    # How many groups?
    def createGroups(self, num):
        if num > 1:
            d = float('inf')
            for i in range(2, self.max_people):
                if (num % i) <= (num % d):
                    d = i
            num_groups = math.floor(num / d)
            rest = (num % d)

            for i in range(0, int(num_groups)):
                self.groups.append(Group(d))

            for i in range(0, rest):
                g = i % len(self.groups)
                self.groups[g].number += 1
        else:
            if num == 1:
                self.groups.append(Group(num))

    # Groups are set, so we notify the channel
    def sendNotifications(self):
        Utils.log('Sending notifications...')
        s = ''
        for count, group in enumerate(self.groups):
            s += '--- GROUP {0} ---\n'.format(count) + group.printMembers()
        self.postMessage(s)

class Group:
    def __init__(self,num_members):
        self.num_members = num_members
        self.members = [] # leader -> members[0]

    def addMember(self,username):
        self.members.append(username)

    def numMembers(self):
        return self.num_members

    def currentNumMembers(self):
        return len(self.members)

    def printMembers(self):
        s = '- Leader:\n'
        for count, member in enumerate(self.members):
            s += member + '\n'
            if count == 0:
                s += '- Members:\n'
        return s

class Utils:
    def __init__(self):
        # Time management
        self.day = 0
        self.hour = 12
        self.minute = 2
        self.sec = 0

        # Requests
        self.valid_words = ['ok', 'yo', 'me', 'coming', 'voy']

    def currentTimestamp(self):
        return time.mktime(datetime.datetime.now().timetuple())

    def nextDay(self):
        now = datetime.datetime.now()

        if now.weekday() == self.day and now.hour >= self.hour:
            if now.hour == self.hour and now.minute >= self.minute:
                t = datetime.timedelta(days=7)
            elif now.hour == self.hour and now.minute <= self.minute:
                t = datetime.timedelta(days=(7 + self.day - now.weekday()) % 7)
            else: # Cualquier otro caso
                t = datetime.timedelta(days=7)
        else:
            t = datetime.timedelta(days=(7 + self.day - now.weekday()) % 7)

        next = (now + t).replace(hour=self.hour, minute=self.minute, second=self.sec)

        now_time = time.mktime(now.timetuple())
        next_time = time.mktime(next.timetuple())

        return next_time - now_time

    def selectRandomPeople(self,max):
        return random.randint(0,max - 1)

    # Not all messages are valid
    def wantsToCome(self,message):
        return self.valid_words.count(message.lower()) != 0

    @staticmethod
    def log(message,*args):
        print message.format(args)