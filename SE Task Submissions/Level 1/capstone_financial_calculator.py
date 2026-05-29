from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.prompt import FloatPrompt
import math

console = Console()

# 1. Create a nice header/title
console.print(Panel.fit(
    "[bold cyan]Financial Calculator[/bold cyan]", 
    subtitle="v1.0", 
    border_style="bright_blue"
))

# 2. Use a Table to show the options clearly
menu_table = Table(show_header=False, box=None, padding=(0, 2))
menu_table.add_row("[bold yellow]Investment[/bold yellow]", "Calculate interest earned on savings.")
menu_table.add_row("[bold yellow]Bond[/bold yellow]", "Calculate monthly home loan repayments.")

console.print(menu_table)
console.print("-" * 50, style="dim") # A subtle divider line

# 3. Use Rich's Prompt to get the user input
# This automatically handles the "Enter either..." text and looks clean
choice = Prompt.ask(
    "Select an option", 
    choices=["investment", "bond"], 
    default="investment",
    case_sensitive=False
)

console.print(f"\n[green]Success![/green] Proceeding with: [bold underline]{choice}[/bold underline]")

def calc_simple_investment(deposit, rate, years):
    rate = rate / 100
    return deposit * (1 + rate * years)

def calc_compound_investment(deposit, rate, years):
    rate = rate / 100
    return deposit * math.pow((1 + rate), years)

def calc_bond_repayment(value, rate, months):
    rate = (rate/100) / 12
    return (rate * value)/(1 - (1 + rate)**(-months))

if choice == "investment":

    deposit_amount = FloatPrompt.ask("[purple] How much are you depositing for your investment?[/purple]")
    interest_rate = FloatPrompt.ask("[purple]At what interest rate? Only give the number without % sign[/purple]")
    years = FloatPrompt.ask("[purple]and for how many years?[/purple]")
    interest_style = Prompt.ask(
        "[purple]Simple or compound interest?[/purple]",
        choices=["simple", "compound"],
        default="compound",
        case_sensitive=False
        )
    
    if interest_style == "simple":

        result = calc_simple_investment(deposit_amount, interest_rate, years)
        console.print(f"[bold yellow] You will have {result} after {years} years![/bold  yellow]")

    else:

        result = calc_compound_investment(deposit_amount, interest_rate, years)
        console.print(f"[bold yellow] You will have {result} after {years} years![/bold  yellow]")

else:

    house_value = FloatPrompt.ask("[purple]What is the present value of the house?[/purple]")
    interest_rate = FloatPrompt.ask("[purple]At what interest rate? Only give the number without % sign[/purple]")
    months = FloatPrompt.ask("[purple]and for how many months?[/purple]")

    result = calc_bond_repayment(house_value, interest_rate, months)

    console.print(f"[bold yellow]You will have to pay {result} each month!")
