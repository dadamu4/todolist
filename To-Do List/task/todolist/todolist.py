# Write your code here
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default="Nothing to do!")
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def main_menu():
    print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete Task\n0) Exit")


def today_tasks():
    rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()

    print("Today {day} {month}:".format(day=datetime.today().day, month=datetime.today().strftime('%b')))

    if not rows:
        print("Nothing to do!")
    else:
        i = 1
        for row in rows:
            print(str(i) + ". " + row.task)
            i += 1


def week_tasks():
    today = datetime.today()

    for i in range(7):
        week_days = today + timedelta(days=i)

        rows = session.query(Table).filter(Table.deadline == week_days.date()).all()

        print("\n{date} {day} {month}:".format(date=week_days.strftime('%A'), day=week_days.day, month=week_days.strftime('%b')))

        if not rows:
            print("Nothing to do!")
        else:
            i = 1
            for row in rows:
                print(str(i) + ". " + row.task)
                i += 1


def all_tasks():
    rows = session.query(Table).order_by(Table.deadline).all()

    if not rows:
        print("You have no tasks to do!")
    else:
        print("All tasks:")
        i = 1
        for row in rows:
            print("{i}. {task}. {deadline}".format(i=i, task=row.task, deadline=row.deadline.strftime("%#d %b")))
            i += 1


def missed_tasks():
    rows = session.query(Table).filter(Table.deadline < datetime.today()).order_by(Table.deadline).all()

    print("\nMissed tasks:")
    if not rows:
        print("Nothing is missed!\n")
    else:
        i = 1
        for row in rows:
            print("{i}. {task}. {deadline}".format(i=i, task=row.task, deadline=row.deadline.strftime("%#d %b")))
            i += 1
        print("\n")

    return rows


def add_task():
    print("Enter task")
    user_task_input = input()

    print("Enter deadline")
    user_deadline_input = input()
    if not datetime.strptime(user_deadline_input, '%Y-%m-%d'):
        print("Incorrect date format, please write the deadline in this format: YYYY-MM-DD")

    new_row = Table(task=user_task_input, deadline=datetime.strptime(user_deadline_input, '%Y-%m-%d'))
    session.add(new_row)
    session.commit()
    print("The task has been added!")


def delete_task():
    missed_rows = missed_tasks()

    if not missed_rows:
        print("Nothing to delete")
    else:
        print("Choose the number of the task you want to delete:")
        i = 1
        for row in missed_rows:
            print("{i}. {task}. {deadline}".format(i=i, task=row.task, deadline=row.deadline.strftime("%#d %b")))
            i += 1
        user_delete_task_input = int(input())

        specific_row = missed_rows[user_delete_task_input - 1]
        session.delete(specific_row)
        session.commit()

        print("The task has been deleted!")


def exit_program():
    print("Bye!")


main_menu()
user_input = input()

while user_input:
    if user_input == "0":
        exit_program()
        break
    elif user_input == "1":
        today_tasks()
    elif user_input == "2":
        week_tasks()
    elif user_input == "3":
        all_tasks()
    elif user_input == "4":
        missed_tasks()
    elif user_input == "5":
        add_task()
    elif user_input == "6":
        delete_task()

    main_menu()
    user_input = input()
