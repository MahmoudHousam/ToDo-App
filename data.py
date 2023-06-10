from cc import app, db, Todo, TodoList
app.app_context().push()

new_list = TodoList(name="Saturday, 10th")
todo1 = Todo(description="Call Dr Zakria")
todo2 = Todo(description="Arrange Meeting with Ahmed Husien")
todo3 = Todo(description="Download the new movie")

todo1.list = new_list
todo2.list = new_list
todo3.list = new_list


# try:
#     db.session.add(new_list)
#     db.session.commit()
# except Exception:
#     db.session.rollback()
# finally:
#     db.session.close()


new_list = TodoList(name="New Milestone 2.6.2")

try:
    db.session.add(new_list)
    db.session.commit()
except Exception:
    db.session.rollback()

todo4 = Todo(description="EDA Clinics to Operation (Hala)")
todo5 = Todo(description="EDA Cath Dataframe (Hala)")
todo6 = Todo(description="Automate the boring staff")

todo4.list_id = new_list.id
todo5.list_id = new_list.id
todo6.list_id = new_list.id

try:
    db.session.add_all([todo4, todo5, todo6])
    db.session.commit()
except Exception:
    db.session.rollback()
finally:
    db.session.close()
