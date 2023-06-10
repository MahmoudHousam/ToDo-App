import sys
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, render_template, request, jsonify, redirect, url_for, abort

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:WierdScience#23\
@localhost:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# parent model


class TodoList(db.Model):
    __tablename__ = "todolists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship("Todo", backref="list", lazy=True)

# child model


class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey(
        "todolists.id"), nullable=True)

    def __repr__(self):
        return f"<ToDo: {self.id}, Description: {self.description}, Completed: {self.completed}>"


@app.route("/todos/create", methods=["POST"])
def create_new_todo():
    description_body = {}
    error = False
    try:
        description = request.get_json()["description"]
        list_id = request.get_json()["list_id"]
        new_todo = Todo(description=description)
        active_list = TodoList.query.get(list_id)
        new_todo.list = active_list
        db.session.add(new_todo)
        db.session.commit()
        description_body["description"] = new_todo.description
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            abort(400)
        else:
            return jsonify(description_body)


@app.route("/todos/<todo_id>/set-completed", methods=["POST"])
def update_todo_status(todo_id):
    try:
        completed = request.get_json()["completed"]
        print('completed', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except Exception:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for("index"))


@app.route("/todos/<todo_id>/set-deleted", methods=["DELETE"])
def delete_todo(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except Exception:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': True})


@app.route('/lists/<list_id>')
def get_todo_by_id(list_id):
    active_list = TodoList.query.get(list_id)
    return render_template('index.html',
                           lists=TodoList.query.all(),
                           active_list=active_list,
                           todos=Todo.query.filter_by(
                               list_id=list_id).order_by('id').all()
                           )


@app.route("/")
def index():
    return redirect(url_for("get_todo_by_id", list_id=1))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
