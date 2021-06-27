from slacker import Slacker
from slackbot.bot import Bot
import os

slack = Slacker(os.environ['API_TOKEN'])
slack.chat.post_message('#slackbot-app', 'new version bot is deployed.', as_user=True)

mybot = Bot()
mybot.run()
