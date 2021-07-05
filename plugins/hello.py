from slackbot.bot import respond_to

@respond_to('hello')
def respond_hello(message):
    message.reply('こんにちは')
