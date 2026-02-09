# Triathlon Award Determiner Thingy (Swim, Cycle, Run)

awards = {
    100: "Provincial colours!",
    105: "Provincial half colours!",
    110: "Provincial scroll!",
    float('inf'): "No award, sorry :("
}

def get_int_input(prompt):
    while True:
        try:
            minutes = int(input(prompt))
            if minutes > 0:
                return minutes
            else:
                print("Can't be negative minutes unless you are a superhero?")
        except ValueError:
            print("Please enter a valid number.")

def ask_time():
    swim_time = get_int_input("Swim time? ")
    cycle_time = get_int_input("Cycle time? ")
    run_time = get_int_input("Run time? ")
    return [swim_time, cycle_time, run_time]

total_time = sum(ask_time())

def determine_award(total_time):

    for key in sorted(awards):
        if total_time <= key:
            return awards[key]
          
print(determine_award(total_time))