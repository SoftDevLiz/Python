import math


# 1. Create a simple header/title
print("=" * 50)
print("        Finance Calculator")
print("=" * 50)

# 2. Show the options clearly
print("\nInvestment - to calculate the amount of interest you'll earn on your investment.")
print("Bond       - to calculate the amount you'll have to pay on a home loan.")
print("-" * 50)

# 3. Get the user input
choice = input(
    "\nEnter either 'investment' or 'bond' from the menu above to proceed: "
).strip().lower()

# Validate the user's choice
while choice not in ["investment", "bond"]:
    choice = input(
        "Invalid choice. Please enter 'investment' or 'bond': "
    ).strip().lower()

print(f"\nProceeding with: {choice}")


def calc_simple_investment(deposit, rate, years):
    """
    Calculate the final amount using simple interest.
    """
    rate = rate / 100
    return deposit * (1 + rate * years)


def calc_compound_investment(deposit, rate, years):
    """
    Calculate the final amount using compound interest.
    """
    rate = rate / 100
    return deposit * math.pow((1 + rate), years)


def calc_bond_repayment(value, rate, months):
    """
    Calculate the monthly repayment amount for a home loan bond.
    """
    rate = (rate / 100) / 12
    return (rate * value) / (1 - (1 + rate) ** (-months))


if choice == "investment":

    deposit_amount = float(
        input("\nHow much are you depositing for your investment? ")
    )

    interest_rate = float(
        input("At what interest rate? (without % sign): ")
    )

    years = float(
        input("For how many years? ")
    )

    interest_style = input(
        "Simple or compound interest? "
    ).strip().lower()

    # Validate the interest type
    while interest_style not in ["simple", "compound"]:
        interest_style = input(
            "Please enter either 'simple' or 'compound': "
        ).strip().lower()

    if interest_style == "simple":

        result = calc_simple_investment(
            deposit_amount,
            interest_rate,
            years
        )

        print(
            f"\nYou will have {result:.2f} after {years} years!"
        )

    elif interest_style == "compound":

        result = calc_compound_investment(
            deposit_amount,
            interest_rate,
            years
        )

        print(
            f"\nYou will have {result:.2f} after {years} years!"
        )

elif choice == "bond":

    house_value = float(
        input("\nWhat is the present value of the house? ")
    )

    interest_rate = float(
        input("At what interest rate? (without % sign): ")
    )

    months = float(
        input("For how many months? ")
    )

    result = calc_bond_repayment(
        house_value,
        interest_rate,
        months
    )

    print(
        f"\nYou will have to pay {result:.2f} each month!"
    )
