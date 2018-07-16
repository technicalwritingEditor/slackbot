import utils
import threading

class App():
    def __init__(self):
        self.bot = utils.Bot()

    # How much time remaining for next Friday?
    # The process will sleep until the day and time is reached
    def run(self):
        while True:
            waiting_time = self.bot.findNextDay()
            print 'Sleeping for ' + str(waiting_time) + ' seconds . . .'
            threading._sleep(waiting_time)
            self.whosComming()

    # The bot will start its work here
    def whosComming(self):
        self.bot.start()
        self.bot.findPeople()
        self.bot.arrangeGroups()
        self.bot.sendNotifications()

if __name__ == "__main__":
    app = App()
    app.run()