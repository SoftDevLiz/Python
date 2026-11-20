def hotel_cost(num_nights):
    """Calculate the total cost of hotel stay based on the number of nights."""
    price_per_night = 1200.00
    return num_nights * price_per_night


def plane_cost(city_flight):
    """Return the flight cost based on the chosen
        South African destination city."""
    city = city_flight.lower()
    if city == "cape town":
        return 2500
    elif city == "durban":
        return 1800
    elif city == "johannesburg":
        return 1500
    elif city == "kruger national park":
        return 3200
    else:
        return 0


def car_rental(rental_days):
    """Calculate the total cost of car rental based on the number of days."""
    daily_rate = 450
    return rental_days * daily_rate


def holiday_cost(num_nights, city_flight, rental_days):
    """Calculate and return the total holiday cost by aggregating hotel."""
    total_hotel = hotel_cost(num_nights)
    total_plane = plane_cost(city_flight)
    total_car = car_rental(rental_days)
    return total_hotel + total_plane + total_car


def get_valid_number(prompt):
    """Prompt the user for a non-negative integer input until valid."""
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
            print("Please enter a number that is 0 or greater.")
        except ValueError:
            print("Invalid input. Please enter a valid whole number.")


def main():
    """Run the main interactive holiday cost calculator."""
    destinations = {
        "1": "Cape Town",
        "2": "Durban",
        "3": "Johannesburg",
        "4": "Kruger National Park",
    }

    print("=" * 50)
    print("      SOUTH AFRICAN HOLIDAY COST CALCULATOR      ")
    print("=" * 50)
    print("\nAvailable Destinations:")
    for key, city in destinations.items():
        print(f"  {key}. {city} (Flight: R{plane_cost(city):,.2f})")

    # City selection loop
    while True:
        choice = input("\nSelect a destination number (1-4): ").strip()
        if choice in destinations:
            city_flight = destinations[choice]
            break
        print("Invalid choice. Please select a valid option from 1 to 4.")

    # Get duration inputs
    num_nights = get_valid_number("Enter the number of nights at the hotel: ")
    rental_days = get_valid_number("Enter the number of days for car rental: ")

    # Calculate individual and total costs
    cost_hotel = hotel_cost(num_nights)
    cost_flight = plane_cost(city_flight)
    cost_car = car_rental(rental_days)
    total_cost = holiday_cost(num_nights, city_flight, rental_days)

    # Display clear summary
    print("\n" + "=" * 50)
    print("             HOLIDAY COST BREAKDOWN              ")
    print("=" * 50)
    print(f" Destination City : {city_flight}")
    print(f" Hotel Stay       : {num_nights} night(s) @ R1,200.00/night")
    print(f" Car Rental       : {rental_days} day(s)   @ R450.00/day")
    print("-" * 50)
    print(f" Hotel Total      : R{cost_hotel:,.2f}")
    print(f" Flight Cost      : R{cost_flight:,.2f}")
    print(f" Car Rental Total : R{cost_car:,.2f}")
    print("=" * 50)
    print(f" TOTAL HOLIDAY COST : R{total_cost:,.2f}")
    print("=" * 50)


if __name__ == "__main__":
    main()
