import time
import os
import json
import csv

class ExpenseTracker:
    def __init__(self, DB="db/Expenses.json"):
        if not os.path.exists(DB):
            with open("db/Expenses.json", "w") as f:
                Expenses = {}
                json.dump(Expenses, f, indent=4)
        self.load_data()

    def load_data(self):
        with open("db/Expenses.json", "r") as f:
            self.data = json.load(f)

    def save_data(self):
        with open("db/Expenses.json","w") as f:
            json.dump(self.data, f, indent=4)

    def add_expenses(self):
        print("Adding Expenses")
        print("-"*len("Adding Expenses"))
        date = input("Enter date(day-mon-year) : ")
        no_of_expenses = int(input("No of expenses : "))
        Expenses_map = {}
        for i in range(no_of_expenses):
            expense = input("Enter the expense category : ")
            amount = int(input("Enter the amount spent : "))
            Expenses_map[expense] = amount
        
        self.data["Expenses"][date] = Expenses_map
        self.save_data()
        print("Expenses data added")
        print()

    def delete_expenses(self):
        print("Deleting Expenses")
        print("-"*len("Deleting Expenses"))
        del_choice = int(input("1. Delete a specific expense \n2. Delete all the expenses of a day \nEnter your choice : "))
        if del_choice == 1:
            del_date = input("Enter the date(day-mon-year) : ")
            if del_date in self.data["Expenses"]:
                print(f"Expenses on day : {del_date}")
                for category,amount in self.data["Expenses"][del_date].items():
                    print(f"{category} : {amount}")

                no_of_dels = int(input("Enter no of expenses you wanna delete : "))
                for i in range(no_of_dels):
                    del_expense = input("Enter the expense category : ")
                    del self.data["Expenses"][del_date][del_expense]
            else:
                print(f"There are no expenses under date '{del_date}'")

        elif del_choice == 2:
            del_date = input("Enter the date(day-mon-year) : ")
            if del_date in self.data["Expenses"]:
                print(f"Expenses on day : {del_date}")
                for category,amount in self.data["Expenses"][del_date].items():
                    print(f"{category} : {amount}")
                tot_del_choice = input(f"Confirm the deletion of total expenses on day '{del_date}' (Y/N) : ").upper()
                if tot_del_choice == "Y":
                    del self.data["Expenses"][del_date]
                    print(f"Deleted total expenses of day : {del_date}")
                elif tot_del_choice == "N":
                    print("Exiting deletion menu...")
            else:
                print(f"There are no expenses under date '{del_date}'")
        self.save_data()

    def edit_expenses(self):
        print("Editing Expenses")
        print("-"*len("Editing Expenses"))
        edit_date = input("Enter the date(day-mon-year) : ")
        if edit_date in self.data["Expenses"]:
            print(f"Expenses on day : {edit_date}")
            for category,amount in self.data["Expenses"][edit_date].items():
                print(f"{category} : {amount}")
            no_of_edits = int(input("Enter no of expenses you wanna delete : "))
            for i in range(no_of_edits):
                edit_expense = input("Enter the expense category : ")
                if edit_expense in self.data["Expenses"][edit_date]:
                    updated_amount = int(input(f"Enter the updated amount for '{edit_expense}'"))
                    self.data["Expenses"][edit_date][edit_expense] = updated_amount
                    print(f"The amount spent on '{edit_expense}' is updated to '{updated_amount}'")
                else:
                    print(f"There's no expenses under category '{edit_expense}'")
        else:
            print(f"There are no expenses under date '{edit_date}'")
        self.save_data()

    def display_expenses(self):
        print("Displaying Expenses")
        print("-"*len("Displaying Expenses"))
        display_date = input("Enter the date to display the expenses(day-mon-year) : ")
        if display_date in self.data["Expenses"]:
            no=0
            print(f"Expenses on day : {display_date}")
            for expense,amount in self.data["Expenses"][display_date].items():
                no+=1
                print(f"{no}. {expense} : {amount}")
        else:
            print(f"There are no expenses under date '{display_date}'")
        
    
    def display_tot_expenses(self,choice):
        print("Printing Total Expenses")
        print("-"*len("Printing Total Expenses"))
        if choice == 3:
            print("Displaying total expenses of a day")
            print("-"*len("Displaying total expenses of a day"))
            display_tot_date = input("Enter the date(day-mon-year) : ")
            if display_tot_date in self.data["Expenses"]:
                tot_expenses_of_the_day = 0
                for category,amount in self.data["Expenses"][display_tot_date].items():
                    tot_expenses_of_the_day+=amount
                    print(f"Expenses on date '{display_tot_date}' \n{category} : {amount}\n")
                print(f"Sum of all expenses on date '{display_tot_date}' : {tot_expenses_of_the_day}")

        elif choice == 4:
            start_date = input("Enter starting date(day-mon-year) : ")
            end_date = input("Enter the end date(day-mon-year) : ")
            s = int(start_date.split("-")[2] + start_date.split("-")[1] + start_date.split("-")[0])
            e = int(end_date.split("-")[2] + end_date.split("-")[1] + end_date.split("-")[0])
            total_amount = 0
            dates_in_range = []
            for date in self.data["Expenses"]:
                d = int(date.split("-")[2]+date.split("-")[1]+date.split("-")[0])
                if s<=d<=e:
                    dates_in_range.append(date)
            
            dates_in_range.sort()
            for D in dates_in_range:
                print(f"\nExpenses on day '{D}'")
                for category,amount in self.data["Expenses"][D].items():
                    print(f"{category} : {amount}")
                    total_amount+=amount
            print(f"\nSum of all expenses b/w dates '{start_date}' and '{end_date}' : {total_amount}")
    
    def export_data(self,choice):
        print("Exporting Data")
        print("-"*len("Exporting Data"))
        if choice == 7:
            rows = []
            for date,expenses in self.data["Expenses"].items():
                for category,amount in expenses.items():
                    rows.append([date,category,amount])

            with open("Whole_expenses_data.csv","w",newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["date","category","amount"])
                writer.writerows(rows)
            print("Data exported successfully, saved as 'Whole_expenses_data.csv'")

        elif choice == 8:
            starting_date = input("Enter starting date(day-mon-year) : ")
            ending_date = input("Enter ending date(day-mon-year) : ")
            s_date = int(starting_date.split("-")[2] + starting_date.split("-")[1] + starting_date.split("-")[0])
            e_date = int(ending_date.split("-")[2] + ending_date.split("-")[1] + ending_date.split("-")[0])
            dates_in_range = []
            for date in self.data["Expenses"]:
                d = int(date.split("-")[2]+date.split("-")[1]+date.split("-")[0])
                if s_date<=d<=e_date:
                    dates_in_range.append(date)
            
            dates_in_range.sort()
            if len(dates_in_range)!=0:
                rows = []
                for date in dates_in_range:
                    for category,amount in self.data["Expenses"][date].items():
                        rows.append([date,category,amount])

                with open(f"Expenses_data_{starting_date}_{ending_date}.csv","w",newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["date","category","amount"])
                    writer.writerows(rows)
                print(f"Data exported successfully, saved as 'Expenses_data_{starting_date}_{ending_date}.csv'")
            else:
                print(f"No expenses found in given range '{starting_date}' to '{ending_date}'")

class Menu:
    def menu(self):
        print("1. Add Expense \n2. Display Expenses of a specific day \n3. Get total expense of a particular day \n4. Get total expense of a week/month \n5. Delete Expenses \n6. Edit Expenses \n7. Export total data \n8. Export expenses data b/w 2 dates \n9. Exit")

    def Choice(self, exp):
        self.menu()
        while True:
            try:
                choice = int(input("Enter your choice : "))
            except Exception:
                print("Enter a valid number")
                continue

            if choice == 1:
                exp.add_expenses()
            
            elif choice == 2:
                exp.display_expenses()

            elif choice == 3 or choice == 4:
                exp.display_tot_expenses(choice)
                
            elif choice == 5:
                exp.delete_expenses()
            
            elif choice == 6:
                exp.edit_expenses()

            elif choice == 7 or choice == 8:
                exp.export_data(choice)

            elif choice == 9:
                print("Exiting expense tracker...")
                break

            else:
                print("\nEnter a Valid input")
                self.menu()

            time.sleep(1)
            print()
            self.menu()
            print("What to do next?")
            print()


def run_expense_tracker():
    print("Welcome to Expense Tracker")
    time.sleep(0.5)
    print("="*len("Welcome to Expense Tracker"))
    time.sleep(0.5)
    print("Select an action to perform")
    Expenses1 = ExpenseTracker(DB="db/Expenses.json")
    menu = Menu()
    menu.Choice(Expenses1)

if __name__=="__main__":
    run_expense_tracker()





