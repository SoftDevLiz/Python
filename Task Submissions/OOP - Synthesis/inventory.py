
# ========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"{self.country} | {self.code} | {self.product} | {self.cost} | {self.quantity}"


# =============Shoe list===========
'''
Stores a list of objects of shoes.
'''
shoe_list = []


# ==========Functions outside the class==============

def update_text_file():
    with open("inventory.txt", "r") as file:
        shoe_data = file.readlines()

    with open("inventory.txt", "w") as file:
        file.write(shoe_data)


def read_shoes_data():
    try:
        with open("inventory.txt", "r") as file:

            try:
                next(file)
            except Exception:
                print("\nThe text file seems to be empty.")

            shoes = file.readlines()

            for shoe_data in shoes:
                country, code, product, cost, quantity = shoe_data[
                    0], shoe_data[1], shoe_data[2], shoe_data[3], shoe_data[4]

                shoe = Shoe(country, code, product, cost, quantity)
                shoe_list.append(shoe)
    except FileNotFoundError:
        print("\nCan't locate the file. Are you in the correct "
              "directory in your terminal?")


def capture_shoes():

    while True:
        try:
            country = input("Country of origin: ")
            code = input("SKU: ")
            product = input("Name: ")
            cost = float(input("Cost: "))
            quantity = int(input("Quantity: "))
            break
        except ValueError:
            print("Oops! Please enter numerical characters "
                  "for cost and quantity.")

    new_shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(new_shoe)

    update_text_file()


def view_all():

    for shoe in shoe_list:
        print(shoe)


def re_stock():

    shoe_to_restock = min(shoe_list, key=lambda shoe: shoe.quantity)

    print("\nThis product is running low:")
    print(f"\n{shoe_to_restock}")

    restock_choice = input(
        "Would you like to restock this shoe? (y/n): ").lower()
    restock_choices = ['y', 'n']

    if restock_choice in restock_choices:

        if restock_choice == 'y':

            while True:
                try:
                    qty_to_order = int(
                        input("How many pairs would you like to order?: "))
                    break
                except ValueError:
                    print("Oops! Please enter numerical characters "
                          "for quantity.")

            shoe_to_restock.quantity += qty_to_order
            update_text_file()

            print(
                f"Success! New quantity for {shoe_to_restock.product} is "
                f"{shoe_to_restock.quantity}.")

        else:
            print("Restock cancelled.")

    else:
        print("Oops! It seems you didn't enter 'y' or 'no'. Returning to main menu.")


def search_shoe():

    provided_sku = input("\nEnter the SKU: ")

    for shoe in shoe_list:
        if shoe.code == provided_sku:
            print("\nShoe found!")
            print(f"\n{shoe}")
            return shoe


def value_per_item():

    print("\nStock Value for Each Product Line:")

    for shoe in shoe_list:
        shoe_value = shoe.get_cost() * shoe.get_quantity()
        print(f"{shoe.code} | {shoe.product} | R{shoe_value}")


def highest_qty():

    overstocked_shoe = max(shoe_list, key=lambda shoe: shoe.quantity)

    print(f"{overstocked_shoe.product} is overstocked and"
          f" will now go on sale!")


# ==========Main Menu=============

while True:

    read_shoes_data()

    print('-' * 30)
    print("Warehouse Inventory Manager")
    print('-' * 30)

    menu_choice = int(input("1. View All Stock"
                            "2. Add New Product"
                            "3. Restock Lowest Product"
                            "4. SKU Search"
                            "5. Value Per Product"
                            "6. Start Sale For Overstocked Product"
                            ))
