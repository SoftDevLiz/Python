from datetime import datetime
from database import init_db
from models import UserService, TaskService
import user_interface as ui


def main():
    init_db()
    u_service = UserService()
    t_service = TaskService()

    print("TASK MANAGER LOGIN")
    user = input("Username: ")
    pw = input("Password: ")

    if not u_service.authenticate(user, pw):
        print("Login failed. Goodbye.")
        return

    print(f"\nWelcome, {user}!")
    while True:
        is_admin = (user == 'admin')
        choice = ui.show_menu(is_admin)

        if choice == 'r' and is_admin:
            new_u = input("New username: ")
            new_p = input("New password: ")
            if u_service.register(new_u, new_p):
                print("Registration successful!")
            else:
                print("Error: User already exists.")

        elif choice == 'a':
            target = input("Assign to: ")
            title = input("Title: ")
            desc = input("Description: ")
            due = input("Due (DD MMM YYYY): ")
            assigned = datetime.now().strftime("%d %b %Y")
            t_service.add_task(target, title, desc, assigned, due)
            print("Task created!")

        elif choice == 'va':
            tasks = t_service.get_all_tasks()
            ui.display_task_table(tasks, "ALL TASKS")

        elif choice == 'vm':
            tasks = t_service.get_user_tasks(user)
            ui.display_task_table(tasks, f"{user}'S TASKS")

        elif choice == 'e':
            print("Closing application.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
