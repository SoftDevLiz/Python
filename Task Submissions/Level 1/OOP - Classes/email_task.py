# --- OOP Email Simulator --- #

# --- Email Class --- #


class Email():
    def __init__(self, email_address, subject_line, email_content):
        self.email_address = email_address
        self.subject_line = subject_line
        self.email_content = email_content
        self.has_been_read = False

    def mark_as_read(self):
        self.has_been_read = True


# --- Functions --- #


def populate_inbox():

    data = [
        ("liz@hyperion.com", "Upskilling", "Hi! I'm loving upskilling!"),
        ("support@hyperion.com", "Help", "I forgot my password."),
        ("boss@hyperion.com", "Meeting", "Are we still on for 2 PM?")
    ]

    for sender, subject, content in data:
        new_email = Email(sender, subject, content)
        inbox.append(new_email)


def list_emails():
    for i, email in enumerate(inbox, start=1):
        print(f"{i} {email.subject_line}")


def read_email(index):
    index = index - 1
    email = inbox[index]
    email.mark_as_read()

    print(f"From: {email.email_address}")
    print(f"Subject: {email.subject_line}")
    print(f"Message: {email.email_content}")


def view_unread_emails():
    for i, email in enumerate(inbox, start=1):
        if email.has_been_read is False:
            print(f"{i} {email.subject_line}")


# --- Lists --- #

inbox = []

# --- Email Program --- #

populate_inbox()

while True:
    user_choice = int(
        input(
            """\nWould you like to:
    1. View all emails
    2. Read an email
    3. View unread emails
    4. Quit application

    Enter selection: """
        )
    )

    if user_choice == 1:
        list_emails()
        pass

    elif user_choice == 2:
        index = int(input("Enter the number of the email you'd like to read "))
        read_email(index)
        pass

    elif user_choice == 3:
        view_unread_emails()
        pass

    elif user_choice == 4:
        print("Goodbye!")
        break

    else:
        print("Oops - incorrect input.")
