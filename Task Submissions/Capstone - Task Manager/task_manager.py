# ===== Importing external modules ===========
import os
from datetime import datetime
from tabulate import tabulate

now = datetime.now()
CURRENT_USER = ''
users = {}
tasks = []

# ==== Helper Functions ====


def load_users():
    """
    Reads usernames and passwords from user.txt and populates the global
    users dictionary. Each line in the file should follow the format:
    username, password.
    """
    with open('user.txt', 'r') as file:

        for line in file:
            parts = line.strip().split(', ')

            if len(parts) == 2:
                username, password = parts
                users[username] = password


def load_tasks():
    """
    Reads task data from tasks.txt and populates the global
    tasks list with dictionaries. Filters out empty lines
    and ensures each task has all six required data fields.
    """
    tasks.clear()
    with open('tasks.txt', 'r') as file:

        for line in file:

            if not line.strip():
                continue

            parts = line.strip().split(', ')

            if len(parts) == 6:
                task_dict = {
                    'username': parts[0],
                    'title': parts[1],
                    'description': parts[2],
                    'assigned_date': parts[3],
                    'due_date': parts[4],
                    'completed': parts[5]
                }
                tasks.append(task_dict)


def update_text_file():
    """
    Overwrites the tasks.txt file with the current data
    stored in the global tasks list. Ensures correct formatting
    and avoids trailing empty lines in the text file.
    """
    with open('tasks.txt', 'w') as file:
        for i, t in enumerate(tasks):
            line = f"{t['username']}, {t['title']}, {t['description']}, {t['assigned_date']}, {t['due_date']}, {t['completed']}"

            if i < len(tasks) - 1:
                file.write(line + "\n")
            else:
                file.write(line)

# ==== Functions ====


def reg_user():
    """
    Prompts for a new username and password, validates that the user
    doesn't already exist, ensures passwords match, and appends to user.txt.
    """
    while True:
        new_username = input("\nNew username: ")

        if new_username in users:
            print("\nError: User already exists. "
                  "Please try a different username.")
            continue

        new_password = input("New password: ")
        confirm_password = input("Confirm password: ")

        if new_password != confirm_password:
            print("\nError: Passwords do not match. Please try again.")
            continue

        try:
            with open('user.txt', 'a') as file:
                file.write(f"\n{new_username}, {new_password}")

            users[new_username] = new_password
            print(f"\nSuccess: Account for '{new_username}' registered!")
            break

        except IOError:
            print("\nError: Could not write to user.txt. "
                  "Please check file permissions.")
            break


def add_task():
    """
    Prompts the user for task details
    (assigned user, title, description, due date) and appends a
    new task to tasks.txt with the current date as the assigned date.
    """
    user = input("Assign a user: ")
    title = input("Task title: ")
    desc = input("Task description: ")
    date_assigned = now.strftime("%d %b %Y")
    due_date = input("Due date (DD MMM YYYY): ")

    with open('tasks.txt', 'a') as file:
        file.write(
            f"\n{user}, {title}, {desc}, {date_assigned}, {due_date}, No")

    print("\nTask added!")


def view_all():
    """
    Displays all tasks currently stored in tasks.txt in a user-friendly
    table format. Uses the tabulate module for clear data labeling
    and readability.
    """
    load_tasks()

    if not tasks:
        print("\nNo tasks have been assigned yet.")
        return

    headers = [
        "No.", "User", "Title", "Description",
        "Assigned Date", "Due Date", "Complete?"
    ]

    table_data = []
    for index, task in enumerate(tasks, 1):
        table_data.append([
            index,
            task['username'],
            task['title'],
            task['description'],
            task['assigned_date'],
            task['due_date'],
            task['completed']
        ])

    print("\n" + "="*30 + " ALL TASKS " + "="*30)
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    # ==== Login Section ====


def view_mine():
    """
    Displays only the tasks assigned to the currently logged-in user.
    Allows the user to select a task by its index number to either mark it as
    complete or edit its details.
    """
    headers = [
        "No.", "User", "Title", "Description",
        "Assigned Date", "Due Date", "Complete?"
    ]

    table_data = []
    for index, task in enumerate(tasks, 1):

        if task['username'] == CURRENT_USER:
            table_data.append([
                index,
                task['username'],
                task['title'],
                task['description'],
                task['assigned_date'],
                task['due_date'],
                task['completed']
            ])

    print("\n" + "="*30 + f" {CURRENT_USER} TASKS " + "="*30)
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    print("=" * 77 + "\n")

    while True:

        choice = input(
            "Enter the No. of the task to edit, "
            "or '-1' to return to menu: ")

        try:
            choice = int(choice)

            if choice == -1:
                break

            task_index = choice - 1

            if 0 <= task_index < len(tasks) and tasks[task_index]['username'] == CURRENT_USER:
                selected_task = tasks[task_index]

                action = input(
                    "Select an option: \n1. Mark as complete\n"
                    "2. Edit task\n: ")

                if action == '1':

                    selected_task['completed'] = "Yes"
                    print("Task marked as complete!")

                elif action == '2':

                    if selected_task['completed'] == "No":
                        edit_choice = input(
                            "Edit: \n1. Assigned Username\n"
                            "2. Due Date\n: ")

                        if edit_choice == '1':
                            new_user = input("Enter new username: ")
                            selected_task['username'] = new_user
                        elif edit_choice == '2':
                            new_date = input(
                                "Enter new due date (DD MMM YYYY): ")
                            selected_task['due_date'] = new_date
                        print("Task updated!")
                    else:
                        print("Error: Completed tasks cannot be edited.")

                update_text_file()
                break
            else:
                print("Invalid task number. Please try again.")

        except ValueError:
            print("Invalid input. Please enter a number.")


def view_completed():
    """
    Filters and displays all tasks that have
    been marked as 'Yes' for completion.
    """
    headers = [
        "No.", "User", "Title", "Description",
        "Assigned Date", "Due Date", "Complete?"
    ]

    table_data = []
    for index, task in enumerate(tasks, 1):

        if task['completed'] == "Yes":
            table_data.append([
                index,
                task['username'],
                task['title'],
                task['description'],
                task['assigned_date'],
                task['due_date'],
                task['completed']
            ])

    print("\n" + "="*30 + " COMPLETED TASKS " + "="*30)
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    print("=" * 77 + "\n")


def delete_task():
    """
    Allows the admin to select a specific task by its
    index number and permanently remove it from the tasks
    list and tasks.txt file.
    """
    view_all()

    if not tasks:
        return

    try:
        task_no = int(
            input("\nEnter the No. of the "
                  "task to delete (or -1 to go back): "))

        if task_no == -1:
            return

        index = task_no - 1

        if 0 <= index < len(tasks):

            removed_task = tasks.pop(index)

            update_text_file()
            print(f"Successfully deleted task: {removed_task['title']}")
        else:
            print("Invalid task number.")

    except ValueError:
        print("Invalid input. Please enter a numeric value.")


def generate_reports():
    """
    Calculates statistics regarding tasks and users
    then generates two text reports:
    task_overview.txt and user_overview.txt.
    Calculations include completion rates and overdue status
    based on the current date.
    """
    # 1. --- Task Overview Calculations ---
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task['completed'] == 'Yes')
    uncompleted_tasks = total_tasks - completed_tasks

    # Calculate overdue tasks (Uncompleted AND date < today)
    overdue_tasks = 0
    curr_date = now

    for task in tasks:
        if task['completed'] == 'No':
            # Convert string date to datetime object for comparison
            due_date = datetime.strptime(task['due_date'], "%d %b %Y")
            if due_date < curr_date:
                overdue_tasks += 1

    # Avoid division by zero if there are no tasks
    perc_incomplete = (uncompleted_tasks / total_tasks *
                       100) if total_tasks > 0 else 0
    perc_overdue = (overdue_tasks / total_tasks *
                    100) if total_tasks > 0 else 0

    # Write task_overview.txt
    with open('task_overview.txt', 'w') as file:
        file.write(f"Total tasks: {total_tasks}\n")
        file.write(f"Completed tasks: {completed_tasks}\n")
        file.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        file.write(f"Overdue tasks: {overdue_tasks}\n")
        file.write(f"Percentage incomplete: {perc_incomplete:.2f}%\n")
        file.write(f"Percentage overdue: {perc_overdue:.2f}%\n")

        # 2. --- User Overview Calculations ---
    total_users = len(users)

    with open('user_overview.txt', 'w') as file:
        file.write(f"Total users: {total_users}\n")
        file.write(f"Total tasks: {total_tasks}\n\n")

        for user in users:
            user_tasks = [task for task in tasks if task['username'] == user]
            u_total = len(user_tasks)
            u_completed = sum(
                1 for task in user_tasks if task['completed'] == 'Yes')
            u_uncompleted = u_total - u_completed

            # User specific overdue
            u_overdue = 0
            for task in user_tasks:
                if task['completed'] == 'No':
                    if datetime.strptime(task['due_date'], "%d %b %Y") < curr_date:
                        u_overdue += 1

            # Percentages for specific user
            perc_assigned = (u_total / total_tasks *
                             100) if total_tasks > 0 else 0
            perc_u_comp = (u_completed / u_total * 100) if u_total > 0 else 0
            perc_u_uncomp = (u_uncompleted / u_total *
                             100) if u_total > 0 else 0
            perc_u_overdue = (u_overdue / u_total * 100) if u_total > 0 else 0

            file.write(f"User: {user}\n")
            file.write(f"  Tasks assigned: {u_total}\n")
            file.write(f"  % of total tasks: {perc_assigned:.2f}%\n")
            file.write(f"  % completed: {perc_u_comp:.2f}%\n")
            file.write(f"  % must still complete: {perc_u_uncomp:.2f}%\n")
            file.write(f"  % overdue: {perc_u_overdue:.2f}%\n")
            file.write("-" * 30 + "\n")

        print("\nReports generated successfully!")


def display_statistics():
    """
    Reads and prints the contents of the report files to the screen.
    If report files do not exist, it triggers generate_reports() first.
    """
    if not os.path.exists('task_overview.txt') or not os.path.exists('user_overview.txt'):
        print("\nReports not found. Generating now...")
        generate_reports()

    print("\n" + "="*20 + " TASK STATISTICS " + "="*20)

    try:
        with open('task_overview.txt', 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print("Error: Could not read task_overview.txt")

    print("\n" + "="*20 + " USER STATISTICS " + "="*20)

    try:
        with open('user_overview.txt', 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print("Error: Could not read user_overview.txt")

    print("="*57 + "\n")

# ==== Login ====


def login():
    """
    Prompts for username and password against the users dictionary.
    Updates the global CURRENT_USER variable upon a successful match.
    """
    global CURRENT_USER

    while True:
        username = input("\nUsername: ")
        password = input("Password: ")

        if username in users:

            if password == users[username]:
                print("\nLogin Successful!")
                CURRENT_USER = username
                break
            else:
                print(f"\nWrong password for {username}.")

        else:
            print("\nNo such account exists.")


load_users()
load_tasks()
login()

# ==== Main Menu Loop ====

while True:

    if CURRENT_USER == 'admin':
        menu = input(
            '''\nSelect one of the following options:
        r - register a user
        a - add task
        va - view all tasks
        vm - view my tasks
        vc - view completed tasks
        del - delete tasks
        gr - generate reports
        ds - display statistics
        e - exit
        : '''
        ).lower()
    else:
        menu = input(
            '''\nSelect one of the following options:
        a - add task
        va - view all tasks
        vm - view my tasks
        e - exit
        : '''
        ).lower()

    if menu == 'r' and CURRENT_USER == 'admin':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'vc' and CURRENT_USER == 'admin':
        view_completed()
    elif menu == 'del' and CURRENT_USER == 'admin':
        delete_task()
    elif menu == 'gr' and CURRENT_USER == 'admin':
        generate_reports()
    elif menu == 'ds' and CURRENT_USER == 'admin':
        display_statistics()
    elif menu == 'e':
        print('Exiting...')
        exit()
    else:
        print("\nInvalid input. Please try again.")
