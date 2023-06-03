import sys
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, jsonify, redirect, url_for, abort

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:WierdScience#23\
@localhost:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr(self):
        return f"<ToDo: {self.id}, Description: {self.description}>"


with app.app_context():
    db.create_all()


@app.route("/todos/create", methods=["POST"])
def create_new_todo():
    description_body = {}
    error = False
    try:
        description = request.get_json()["description"]
        new_todo = Todo(description=description)
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


@app.route("/")
def index():
    return render_template("index.html", data=Todo.query.all())


if __name__ == "__main__":
    app.run(debug=True, port=5000)
