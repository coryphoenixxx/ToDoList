from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_text')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f"{self.task}"


Base.metadata.create_all(engine)


while True:
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
    user_choice = int(input())
    if user_choice == 0:
        print("\nBye!")
        break
    #########1#########
    elif user_choice == 1:
        print(f"\nToday {datetime.today().day} {datetime.now().strftime('%b')}:")
        today = datetime.today()
        tasks = session.query(Task).filter(Task.deadline == today.date()).all()
        if not tasks:
            print("Nothing to do!\n")
        else:
            for task in tasks:
                print(task.__repr__())
            print()
    #########2#########
    elif user_choice == 2:
        today = datetime.today()
        for i in range(0,7):
            day = today + timedelta(days=i)
            print('\n' + day.strftime('%A'), day.strftime('%d'), day.strftime('%b') + ':')
            tasks = session.query(Task).filter(Task.deadline == day.date()).all()
            if not tasks:
                print("Nothing to do!")
            else:
                for task in tasks:
                    print(f"{tasks.index(task)+1}. {task.task}")
        print()
    #########3#########
    elif user_choice == 3:
        print("\nAll tasks:")
        tasks = session.query(Task).order_by(Task.deadline).all()
        if not tasks:
            print("Nothing is missed!")
        else:
            for task in tasks:
                print(f"{tasks.index(task)+1}. {task.task}", end='. ')
                print(task.deadline.strftime('%d'), task.deadline.strftime('%b'))
            print()
    #########4#########
    elif user_choice == 4:
        print("\nMissed tasks:")
        today = datetime.today()
        tasks = session.query(Task).filter(Task.deadline < today.date()).all()
        if not tasks:
            print("Nothing is missed!\n")
        else:
            for task in tasks:
                print(f"{tasks.index(task)+1}. {task.task}", end='. ')
                print(task.deadline.strftime('%d'), task.deadline.strftime('%b'))
            print()
    #########5#########
    elif user_choice == 5:
        task = input("\nEnter task\n")
        deadline = list(map(int, input("Enter deadline\n").split('-')))
        user_task = Task(task=task, deadline=datetime(*deadline))
        session.add(user_task)
        session.commit()
        print("The task has been added!\n")
    #########6#########
    elif user_choice == 6:
        print("\nChoose the number of the task you want to delete::")
        tasks = session.query(Task).order_by(Task.deadline).all()
        if not tasks:
            print("Nothing to delete")
        else:
            for task in tasks:
                print(f"{tasks.index(task) + 1}. {task.task}", end='. ')
                print(task.deadline.strftime('%d'), task.deadline.strftime('%b'))
            delete_choice = int(input()) - 1
            session.delete(tasks[delete_choice])
            print("The task has been deleted!\n")
            session.commit()
