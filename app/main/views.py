from flask import render_template, request, redirect, url_for, flash

from app import app
from app.models import Category, Todo, Priority, db
import time


@app.route('/')
def list_all():
    return render_template(
        'list.html',
        categories=Category.query.all(),
        todos=Todo.query.all(),  # join(Priority).order_by(Priority.value.desc())
    )


@app.route('/<name>')
def list_todos(name):
    category = Category.query.filter_by(name=name).first()
    return render_template(
        'list.html',
        # .join(Priority).order_by(Priority.value.desc()),
        todos=Todo.query.filter_by(category=category).all(),
        categories=Category.query.all(),

    )


@app.route('/new-task', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        category = Category.query.filter_by(
            id=request.form['category']).first()
        priority = Priority.query.filter_by(
            id=request.form['priority']).first()
        today = "{}".format(time.strftime("%Y-%m-%d %H:%M:%S"))
        todo = Todo(category=category, priority=priority,
                    creation_date=today, description=request.form['description'])
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('list_all'))
    else:
        return render_template(
            'new-task.html',
            page='new-task',
            categories=Category.query.all(),
            priorities=Priority.query.all()
        )


@app.route('/edit-todo/<int:todo_id>', methods=['GET', 'POST'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if request.method == 'GET':
        return render_template(
            'edit-todo.html',
            todo=todo,
        )
    else:
        updated_todo = request.form['description']
        todo.description = updated_todo
        db.session.commit()
        return redirect('/')


@app.route('/new-category', methods=['GET', 'POST'])
def new_category():
    if request.method == 'POST':
        category = Category(name=request.form['category'])
        db.session.add(category)
        db.session.commit()
        return redirect('/')
    else:
        return render_template(
            'new-category.html',
            page='new-category.html')


@app.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    category = Category.query.get(category_id)
    if request.method == 'GET':
        return render_template(
            'new-category.html',
            category=category
        )
    else:
        category_name = request.form['category']
        category.name = category_name
        db.session.commit()
        return redirect('/')


@app.route('/delete-category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    if request.method == 'POST':
        category = Category.query.get(category_id)
        # if not category.todos:
        db.session.delete(category)
        db.session.commit()
        # else:
        #    flash('You have TODOs in that category. Remove them first.')
        return redirect('/')


@app.route('/delete-todo/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    if request.method == 'POST':
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return redirect('/')


@app.route('/mark-done/<int:todo_id>', methods=['GET', 'POST'])
def mark_done(todo_id):
    # if request.method == 'GET':
    todo = Todo.query.get(todo_id)
    # prio = Priority(id=todo_id, name="low", value=0)
    todo.is_done = True
    todo.creation_date = "done"
    # db.session.add(prio)
    db.session.commit()
    return redirect('/')
