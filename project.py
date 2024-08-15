# Imports
import sys
from pyfiglet import Figlet
import matplotlib.pyplot as plt
import pandas as pd
import csv

# Import assets csv file
try:
    df = pd.read_csv('mybudget.csv')

except FileNotFoundError:
    data = [
        ["account", "amount"],
        ["daily checkings", "0.00"],
        ["monthly checkings", "0.00"],
        ["short term savings", "0.00"],
        ["long term savings", "0.00"],
        ["investment portfolio", "0.00"]
    ]

    # Open a file in write mode
    with open('mybudget.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def main():
    # Figlet visual
    f = Figlet(font='slant')
    print(f.renderText('Budget50'))

    # Menu
    while True:
        print("") # auto newline
        print("----------------------------------------------------------------")
        print("Welcome to Budget50! Type the corresponding number to access the features.")
        print("1) Paycheck Calculator")
        print("2) Long Term Savings Calculator")
        print("3) Assets")
        print("4) Expense Visualizer")
        print("Type 'exit' to exit the program.")
        menuClick = input("Option: ")
        print("") # auto newline

        if menuClick == '1':
            pretax = input("Enter your paycheck amount (before taxes, without the dollar sign): ")
            print("") # auto newline
            postTax, needs, wants, savings = paycheckCalculator(float(pretax))

            print("Here's your paycheck divided using the 50/30/20 rule!")
            print("") # auto newline
            print(f"Income after taxes: ${round(postTax, 2)} \nNeeds (debts, rent, necessary food, insurance): ${round(needs, 2)} \nWants (anything you want): ${round(wants, 2)} \nSavings (this amount will go into your savings): ${round(savings, 2)}")
        
        elif menuClick == '2':
            print("This program allows you to estimate the amount of time it will take to save up for a savings goal. Provide the program your savings amount goal and amount deposited each month.")
            print("The program will state the time in months.")
            savingsGoal = input("Savings Goal (don't use the dollar sign): ")
            monthlyDeposit = input("Monthly Deposit (don't use the dollar sign): ")
            print("") # auto newline
            print("It will take you approx. " + str(round(longTermGoal(float(savingsGoal), float(monthlyDeposit)))) + " months to save till your goal!")
        
        elif menuClick == '3':
            print(assets() + "\n")
            answer = input("Do you need to update your assets? Please type 'yes' or 'no'.\n")
            if answer == 'yes':
                update_assets()
            elif answer == 'no':
                print("Ok.")

        elif menuClick == '4':
            print("Your monthly subscriptions are already included. Indicate additional monthly expenses that you will expect.")
            print("First, confirm if the following subscriptions will be paid for this month by typing 'yes' or 'no'.")
            print("") # auto newline
            expensesVisualizer()
        
        elif menuClick == 'exit':
            sys.exit("Goodbye!")
        
        else:
            raise ValueError
# -------------------
# Functions

def paycheckCalculator(paycheckAmount):
    taxedAmount = paycheckAmount * 0.15
    remainingAmount = paycheckAmount - taxedAmount
    needs = remainingAmount * 0.50
    wants = remainingAmount * 0.30
    savings = remainingAmount * 0.20
    return (remainingAmount, needs, wants, savings)

def expensesVisualizer():
    # Default monthly expenses
    expensesList = {
        "planet fitness": 26.99,
        "spotify": 5.99
    }

    # Confirm default payments still processed this month and add additional expected monthly payments
    for x in ["Planet Fitness", "Spotify"]:
        confirm = input(x + "? ")
        if confirm.lower() == "yes":
            pass
        elif confirm.lower() == "no":
            del expensesList[confirm.lower()]

    # Add the additional monthly expenses that you expect.
    print("") # auto newline
    print("Now, report your additional monthly expenses.")
    print("Report by writing the expense name, then colon, then the expense amount.")
    print("") # auto newline
    print("Example: 'walmart:104.32'")
    print("") # auto newline
    print("Avoid parentheses for the expense names. Type 'None' if you have no expenses to report or when finished reporting.")
    print("") # auto newline

    while True:
        otherExpense = input("Other Expected Monthly Expenses: ")

        if otherExpense == "None":
            break
        else:
            try:
                tempEx = otherExpense.split(':')
                expensesList[tempEx[0]] = float(tempEx[1])
            except IndexError:
                sys.exit("Damn bruh you typed an incorrect value.")

    # Generate a total for all expenses, and append the two arrays for plotting
    total = 0
    itemsArr = []
    sizes = []

    for item in expensesList:
        total += expensesList[item]
        itemsArr.append(item)

    for item in expensesList:
        percent = round((expensesList[item] / total) * 100)
        sizes.append(percent)

    # Plot!
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=itemsArr)
    plt.show()

def longTermGoal(goal, monthlyDeposit):
    if monthlyDeposit == 0:
        raise ZeroDivisionError

    return goal / monthlyDeposit

def assets():
    return df.to_string(index=False) # type: ignore

def update_assets():
    print("Follow the prompt by typing amounts only. Do not write 'yes' or 'no'. Rewrite the amount if necessary.")
    for elem in ["daily checkings", "monthly checkings", "short term savings", "long term savings", "investment portfolio"]:
        updated = input(elem + "? ")
        updated = float(updated)
        if updated == 0.0:
            pass
        else:
            df.loc[(df['account'] == elem), 'amount'] = updated # type: ignore

    df.to_csv('mybudget.csv', index=False) # type: ignore
    return df.to_string(index=False) # type: ignore

if __name__ == '__main__':
    main()
