import dataset
from datetime import datetime

class TodoDB(object):
  def __init__(self):
    db = dataset.connect("sqlite:///db.sqlite")
    self.table = db.create_table('todo', primary_increment=True)

  def add(self, title, limit_at):
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    self.table.insert({"title": title, "importance": 1, "limit_at": limit_at, "updated_at": updated_at})

  def imp(self, title, limit_at):
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    self.table.insert({"title": title, "importance": 10, "mark":chr(int("10071")), "limit_at": limit_at, "updated_at": updated_at})

  def hw(self, title, limit_at):
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    self.table.insert({"title": title, "importance": 15, "mark":chr(int("128221")), "limit_at": limit_at, "updated_at": updated_at})

  def update(self, todo_id, title = None, limit_at = None):
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if title is not None:
      self.table.update({"id": todo_id, "title": title, "updated_at": updated_at}, ["id"])
    if limit_at is not None:
      self.table.update({"id": todo_id, "limit_at": limit_at, "updated_at": updated_at}, ["id"])

  def find_title(self, title = None):
    if title is not None:
      return self.table.find(title = {'like': '%' + title + '%'})
    else:
      return None

  def find_date(self, limit_at = None):
    if limit_at is not None:
      return self.table.find(limit_at = {'like': '%' + limit_at + '%'})
    else:
      return None

  def all(self):
    return self.table.find(order_by=['-importance'])
    #return self.table.all()

  def delete(self, todo_id):
    self.table.delete(id=todo_id)