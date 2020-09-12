# Write your code here
from operator import and_
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

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

def print_menu():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    users_choice = int(input())
    compare_users_choice(users_choice)
def compare_users_choice(users_choice):
    today = datetime.today()
    if users_choice == 0:
        print("Bye")
        return None
    elif users_choice == 1:
        rows = session.query(Table).filter(Table.deadline == datetime.date(today)).all()
        if rows == []:
            print("Today", today.day, today.strftime('%b'), ":\nNothing to do!")
        else:
            count = 1
            print("Today:", today.day, today.strftime('%b'))
            for row in rows:
                print("{0}. {1}".format(count, row))
                count += 1
        print("\n")
        print_menu()
    elif users_choice == 2:
        rows = session.query(Table).order_by(Table.deadline).filter(
            Table.deadline <= today.date() + timedelta(days=7))
        week = [today.date() + timedelta(days=i) for i in range(7)]
        row_dict = {row: row.deadline for row in rows}
        for myday in week:
            if myday in row_dict.values():
                print(f'\n{myday.strftime("%A")} {myday.day} {myday.strftime("%b")}')
                for entry in rows:
                    if entry.deadline == myday:
                        print(f'{entry.id}. {entry}')
            else:
                print(f'\n{myday.strftime("%A")} {myday.day} {myday.strftime("%b")}')
                print('Nothing to do!\n')
        print_menu()
    elif users_choice == 3:
        rows = session.query(Table).all()
        if rows == []:
            print("All tasks: \n1. Nothing to do")
        else:
            count = 1
            tasks = session.query(Table).order_by(Table.deadline).all()
            print("All tasks:")
            for task in tasks:
                print("{0}. {1}. {2} {3}".format(count, task, task.deadline.day, task.deadline.strftime('%b')))
                count += 1
            print("\n")
            print_menu()
    elif users_choice == 4:
        print("Missed tasks: ")
        count = 1
        tasks = session.query(Table).filter(Table.deadline < datetime.date(today)).all()
        if tasks == []:
            print("Nothing is missed!")
        else:
            for task in tasks:
                print("{0}. {1}. {2} {3}".format(count, task, task.deadline.day, task.deadline.strftime('%b')))
                count += 1
        print("\n")
        print_menu()
    elif users_choice == 5:
        print("Enter task")
        task_input = input()
        print("Enter deadline")
        deadline_time = input()
        deadline_time = datetime.strptime(deadline_time, "%Y-%m-%d")
        new_row = Table(task=task_input,deadline=deadline_time)
        session.add(new_row)
        session.commit()
        print("The task has been added!\n")
        print_menu()
    elif users_choice == 6:
        print("Choose the number of the task you want to delete:")
        count = 1
        tasks = session.query(Table).order_by(Table.deadline).all()
        print("All tasks:")
        if tasks == []:
            print("Nothing to delete\n")
            print_menu()
        else:
            for task in tasks:
                print("{0}. {1}. {2} {3}".format(count, task, task.deadline.day, task.deadline.strftime('%b')))
                count += 1
            to_delete = int(input())
            to_delete -= 1
            session.delete(tasks[to_delete])
            session.commit()
            print("The task has been deleted!")
            print_menu()
print_menu()
