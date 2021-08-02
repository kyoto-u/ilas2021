from tododb import TodoDB
from slackbot.bot import respond_to
from slackbot.dispatcher import Message

@respond_to(r'^\s*task\s+(\S+)')
def remind_task(message):
    message.reply()
def get_todo_list():
  todo_table = TodoDB()
  todo_list = todo_table.all()
  msg = ""
  for item in todo_list:
    msg += f"{item['id']}: {item['title']}: {item['limit_at']}\n"
  return msg
