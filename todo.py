from datetime import date
import os.path
from os import path
import sys


def help():
    """
    prints the CLI usage.
    """
    string = ("""Usage :-
$ ./todo add "todo item"  # Add a new todo
$ ./todo ls               # Show remaining todos
$ ./todo del NUMBER       # Delete a todo
$ ./todo done NUMBER      # Complete a todo
$ ./todo help             # Show usage
$ ./todo report           # Statistics""")
    print(string)


def listToDo():
    """
    lists all the todos that are not yet complete 
    in last in first out order.
    """
    with open("todo.txt") as toDoFile:
        tasks = toDoFile.readlines()
        if len(tasks) > 0:
            for index, task in enumerate(tasks, 1):
                print("[{0}] {1}".format(
                    len(tasks) - index + 1, task.strip("\n")))
        else:
            print("There are no pending todos!")


def addToDo(task):
    """
    Adds the todo item to the list
    """
    with open("todo.txt", 'r+') as toDoFile:
        lines = toDoFile.readlines()
        toDoFile.seek(0)
        toDoFile.write(task + "\n")
        for line in lines:
            toDoFile.write(line)
        return True


def delToDo(item):
    """
    Removes the todo item by its number
    """
    with open("todo.txt", 'r+') as toDoFile:
        tasks = toDoFile.readlines()
        if 0 < item <= len(tasks):
            toDoFile.seek(0)
            for index, task in enumerate(tasks, 1):
                taskNo = len(tasks) - index + 1
                if taskNo != item:
                    toDoFile.write(task)
            toDoFile.truncate()
            return True


def doneToDo(item):
    """
    Marks the todo item as completed given its number
    """
    with open("todo.txt") as toDoFile:
        tasks = toDoFile.readlines()
    if delToDo(item):
        completedTask = tasks[len(tasks) - item]
        with open("done.txt", "a") as doneFile:
            doneFile.write("x {0} {1}".format(date.today(), completedTask))
        return True


def report():
    """
    prints the latest tally of pending and completed todos.
    """
    with open("todo.txt") as toDoFile:
        remTasks = toDoFile.readlines()
    with open("done.txt") as doneFile:
        completedTasks = doneFile.readlines()
    print("{0} Pending : {1} Completed : {2}".format(
        date.today(), len(remTasks), len(completedTasks)))


def main():
    # Create the files if they don't exist in the running directory
    if not path.exists("todo.txt"):
        open("todo.txt", 'w')
        open("done.txt", "w")

    if not path.exists("done.txt"):
        open("done.txt", "w")

    functions = {"add": addToDo,
                 "ls": listToDo,
                 "del": delToDo,
                 "done": doneToDo,
                 "help": help,
                 "report": report
                 }
    MissingArgErrorReports = {"add": "Error: Missing todo string. Nothing added!",
                              "del": "Error: Missing NUMBER for deleting todo.",
                              "done": "Error: Missing NUMBER for marking todo as done."
                              }

    if len(sys.argv) == 1:
        help()

    elif len(sys.argv) == 2:
        _, cmd = sys.argv
        if cmd not in ["add", "del", "done"]:
            functions[cmd]()
        else:
            print(MissingArgErrorReports[cmd])

    elif len(sys.argv) == 3:
        _, cmd, arg = sys.argv
        if cmd == "add":
            if addToDo(arg):
                print('Added todo: "{}"'.format(arg))
        elif cmd == "del":
            if delToDo(int(arg)):
                print('Deleted todo #{}'.format(arg))
            else:
                print('Error: todo #{} does not exist. Nothing deleted.'.format(arg))
        elif cmd == "done":
            if doneToDo(int(arg)):
                print('Marked todo #{} as done.'.format(arg))
            else:
                print('Error: todo #{} does not exist.'.format(arg))


if __name__ == "__main__":
    main()
