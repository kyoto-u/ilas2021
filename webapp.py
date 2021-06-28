from flask import Flask, render_template, redirect, url_for, request
from tododb import TodoDB

app = Flask(__name__)

@app.route('/<name>')
def main(name):
  templatename = name + '.html'
  return render_template(templatename, path=name)

@app.route('/todo', methods=['POST'])
def todo():
  if (request.form['_method'] == 'POST'):
    title = request.form['title']
    limit_at = request.form['limit_at']
    todo_table = TodoDB()
    todo_table.add(title, limit_at)

  if (request.form['_method'] == 'DELETE'):
    table_id = int(request.form['table_id'])
    todo_table = TodoDB()
    todo_table.delete(todo_id=table_id)

  return redirect(url_for('todo_get'))

@app.route('/todo', methods=['GET'])
def todo_get():
  todo_table = TodoDB()
  templatename = 'todo.html'
  return render_template(templatename, path='todo', table=todo_table)

@app.route('/')
def root():
  return redirect(url_for('main', name='index'))

if __name__ == '__main__':
  app.run(debug=True)
