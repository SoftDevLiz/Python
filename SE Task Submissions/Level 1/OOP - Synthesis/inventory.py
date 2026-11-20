from tabulate import tabulate

# Colors used in the program


class Colors:
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    END = '\033[0m'
    BOLD = '\033[1m'

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
    '''
    Helper function that rewrites the data
    to the text file based on the in memory
    shoe_list.
    '''
    with open("inventory.txt", "w") as file:
        file.write("Country,Code,Product,Cost,Quantity\n")

        for shoe in shoe_list:
            file.write(
                f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}\n")


def read_shoes_data():
    '''
    Reads the data from the provided text file,
    creates Shoe objects from each line and appends
    it to the shoe_list.
    '''
    try:
        with open("inventory.txt", "r") as file:

            try:
                next(file)
            except Exception:
                print(
                    f"\n{Colors.WARNING}The text file seems to be empty.{Colors.END}")

            shoes = file.readlines()

            for line in shoes:
                data = line.strip().split(',')

                if len(data) == 5:
                    country, code, product, cost, quantity = data
                    shoe = Shoe(country, code, product, cost, int(quantity))
                    shoe_list.append(shoe)
                else:
                    raise Exception(
                        "The length of the data for each shoe is corrupt. Check the text file.")

    except FileNotFoundError:
        print(f"\n{Colors.WARNING}Can't locate the file. Are you in the correct "
              f"directory in your terminal?{Colors.END}")
    except Exception as e:
        print(
            f"\n{Colors.WARNING}Something is wrong with the data: {e} {Colors.END}")


def capture_shoes():
    '''
    Takes new shoe data via user input,
    adds it to the shoe_list and updates the
    text file.
    '''
    while True:
        try:
            print("\n")
            country = input("Country of origin: ")
            code = int(input("SKU Number (Number only): "))
            code = f"SKU{code}"
            product = input("Name: ")
            cost = float(input("Cost: "))
            quantity = int(input("Quantity: "))
            print(f"\n{Colors.SUCCESS}New product added!{Colors.END}")
            break
        except ValueError:
            print(f"\n{Colors.WARNING}Oops! Please enter numerical characters "
                  f"for SKU, cost and quantity.{Colors.END}")

    new_shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(new_shoe)

    update_text_file()


def view_all():
    '''
    Prints out a table of all
    of the current shoes in the 
    inventory based on the shoe_list.
    '''
    table_data = []
    for shoe in shoe_list:
        table_data.append([
            shoe.country,
            shoe.code,
            shoe.product,
            shoe.cost,
            shoe.quantity
        ])

    headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    print("\n" + tabulate(table_data, headers=headers, tablefmt="fancy_grid"))


def re_stock():
    '''
    Finds the shoe with the lowest stock
    and gives the user the option to
    restock that shoe.
    '''

    shoe_to_restock = min(shoe_list, key=lambda shoe: shoe.quantity)

    print("\nThis product is running low:")
    print(f"\n{shoe_to_restock}")

    restock_choice = input(
        "\nWould you like to restock this shoe? (y/n): ").lower()
    restock_choices = ['y', 'n']

    if restock_choice in restock_choices:

        if restock_choice == 'y':

            while True:
                try:
                    qty_to_order = int(
                        input("\nHow many pairs would you like to order?: "))
                    break
                except ValueError:
                    print(f"\n{Colors.WARNING}Oops! Please enter numerical characters "
                          f"for quantity.{Colors.END}")

            shoe_to_restock.quantity += qty_to_order
            update_text_file()

            print(
                f"\n{Colors.SUCCESS}Success! New quantity for {shoe_to_restock.product} is "
                f"{shoe_to_restock.quantity}.{Colors.END}")

        else:
            print("\nRestock cancelled.")

    else:
        print(F"\n{Colors.WARNING}Oops! It seems you didn't enter 'y' or 'no'. Returning to main menu.{Colors.END}")


def search_shoe():
    '''
    Takes user input to search for
    a shoe in the inventory based
    on the SKU.
    '''
    while True:
        try:
            provided_sku = int(input("\nEnter the SKU (Number only): "))
            provided_sku = f"SKU{provided_sku}"
            break
        except ValueError:
            print(
                f"\n{Colors.WARNING}Oops! Enter only the numbers for the SKU.{Colors.END}")

    for shoe in shoe_list:
        if shoe.code == provided_sku:
            print(f"\n{Colors.SUCCESS}Shoe found!{Colors.END}")

            table_data = [[
                shoe.country,
                shoe.code,
                shoe.product,
                shoe.cost,
                shoe.quantity
            ]]

            headers = ["Country", "Code", "Product", "Cost", "Quantity"]

            print("\n" + tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
            return shoe

    print(f"\n{Colors.WARNING}That SKU is not in the current inventory.{Colors.END}")


def value_per_item():
    '''
    Calculates the total stock
    value for each product line
    and prints it out.
    '''
    print(f"\n{Colors.BOLD}Stock Value for Each Product Line:{Colors.END}")

    table_data = []

    for shoe in shoe_list:

        total_value = float(shoe.get_cost()) * int(shoe.get_quantity())

        table_data.append([
            shoe.code,
            shoe.product,
            shoe.get_cost(),
            shoe.get_quantity(),
            f"R{total_value:,.2f}"
        ])

    headers = ["SKU", "Product", "Cost", "Qty", "Total Value"]

    print(tabulate(table_data, headers=headers,
          tablefmt="fancy_grid"))


def highest_qty():
    '''
    Finds the shoe with the most stock
    and prints it out as being for sale.
    '''
    overstocked_shoe = max(shoe_list, key=lambda shoe: shoe.quantity)

    print(f"\n{Colors.SUCCESS}{overstocked_shoe.product} is overstocked and"
          f" will now go on sale!{Colors.END}")


# ==========Main Menu=============

# Loads the shoes from the text file
read_shoes_data()

while True:

    menu = f"""
    {Colors.BOLD}========= Inventory Manager ========={Colors.END}
    1. View All Stock
    2. Add New Product
    3. Restock Lowest Product
    4. SKU Search
    5. Value Per Product
    6. View Sale
    0. Exit
    {Colors.BOLD}====================================={Colors.END}
    Enter your choice: """

    menu_choice = int(input(menu))

    if menu_choice == 1:
        view_all()
    elif menu_choice == 2:
        capture_shoes()
    elif menu_choice == 3:
        re_stock()
    elif menu_choice == 4:
        search_shoe()
    elif menu_choice == 5:
        value_per_item()
    elif menu_choice == 6:
        highest_qty()
    elif menu_choice == 0:
        print(f"\n{Colors.WARNING}Exiting...{Colors.END}")
        break
