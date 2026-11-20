class Course:
    # Class attribute for the course name
    name = "Fundamentals of Computer Science"

    # Class attribute for the contact website
    contact_website = "www.hyperiondev.com"

    head_office = "Cape Town"

    # Method to display contact details
    def contact_details(self):
        print("Please contact us by visiting", self.contact_website)

    # Method to display head office
    def head_office_location(self):
        print(self.head_office)


# Example usage:
# Create an instance of the Course class
course = Course()

# Call the contact_details method to display contact information
course.contact_details()


# Course subclass - OOPCourse
class OOPCourse(Course):

    """Constructor that initializes 'desc', 'trainer' and 'course_ID'
    # with default values"""

    def __init__(self, description="OOP Fundamentals",
                 trainer="Mr Anon A. Mouse", course_ID="#12345"):
        self.description = description
        self.trainer = trainer
        self.course_ID = course_ID

    # Method that prints course desc and trainer name
    def trainer_details(self):
        print(self.description)
        print(self.trainer)

    # Method that prints the course ID
    def show_course_id(self):
        print(self.course_ID)


# OOPCourse subclass object creation
course_1 = OOPCourse()

# Calls inherited + non-inherited methods on the object
course_1.contact_details()
course_1.trainer_details()
course_1.show_course_id()
