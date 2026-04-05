from tabulate import tabulate


def show_menu(is_admin):
    """Displays choices based on user role."""
    menu = "\n--- MENU ---\na - Add Task\nva - View All Tasks\nvm - View My Tasks\ne - Exit"
    if is_admin:
        menu += "\nr - Register User"
    print(menu)
    return input("Select an option: ").lower()


def display_task_table(tasks, title="TASKS"):
    """Formats list of task objects into a clean grid."""
    if not tasks:
        print(f"\nNo data found for {title}.")
        return

    headers = ["ID", "Assigned To", "Title", "Due Date", "Status"]
    # Convert SQLite rows to a format tabulate understands
    table_data = [[t['id'], t['username'], t['title'],
                   t['due_date'], t['completed']] for t in tasks]

    print(f"\n=== {title} ===")
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
