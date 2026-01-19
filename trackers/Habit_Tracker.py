#HABIT TRACKER
import time
import os
import json
import csv
from datetime import datetime,date

class HabitTracker:
    def __init__(self,DB="db/Habits.json"):
        if not os.path.exists(DB):
            with open("db/Habits.json","w") as f:
                json.dump(
                {
                  "habits": []
                },f,
                indent=4
                )
        self.load_data()

    def load_data(self):
        with open("db/Habits.json","r") as f:
            self.data = json.load(f)

    def save_data(self):
        with open("db/Habits.json","w") as f:
            json.dump(self.data,f,indent=4)

    def list_habits(self):
        i=1
        for habit in self.data["habits"]:
            print(f"{i} : {habit["name"]}")
            i+=1
        print()

    def add_habit(self):
        print("Adding Habit")
        print("-"*len("Adding Habit"))
        name = input("Enter the habit which you wanna add : ")
        created_at = date.today().isoformat()
        logs = {}
        is_active = True
        habit = {
                 "name" : name,
                 "Created at" : created_at,
                 "logs" : logs,
                 "log_lst":[],
                 "streak":0,
                 "Is active" : is_active
                }
        self.data["habits"].append(habit)
        self.save_data()
        print(f"Added habit '{name}'")
    
    def delete_habit(self):
        print("Deleteing Habit")
        print("-"*len("Deleteing Habit"))
        self.list_habits()
        name = input("Enter the habit which you wanna delete : ")
        found = False
        for habit in self.data["habits"]:
            if habit["name"]==name:
                target_habit = habit
                found = True
                self.data["habits"].remove(target_habit)
                break
        print(f"Deleted habit '{name}'")        
        if not found:
            print(f"There's no habit '{name}'")
        self.save_data()
        

    def display_habits(self):
        print("Displaying Habits and info")
        print("-"*len("Displaying Habits and info"))
        for habit in self.data["habits"]:
            for key,value in habit.items():
                print(f"{key} : {value}")
            time.sleep(0.5)
            print()
        

    def mark_habit(self):
        print("Marking Habit")
        print("-"*len("Marking Habit"))
        print("Habits")
        print("="*len("Habits"))
        self.list_habits()
        habit_name = input("Enter the habit : ")
        date = input("Enter the date(yyyy-mm-dd) : ")
        found = False
        for habit in self.data["habits"]:
            if habit["name"]==habit_name:
                if date in habit["logs"]:
                    print(f"'{date}' already logged")
                    return
                found=True
                target_habit = habit
                habit["logs"][date]="done"

        if not found:
            print(f"There's no habit '{habit_name}'")
            return 
        
        date_int = datetime.strptime(date, "%Y-%m-%d").toordinal()
        if date_int not in target_habit["log_lst"]:
            target_habit["log_lst"].append(date_int)
            target_habit["log_lst"].sort()

        if len(target_habit["log_lst"]) == 1:
            target_habit["streak"] = 1
        elif target_habit["log_lst"][-1] - target_habit["log_lst"][-2] == 1:
            target_habit["streak"] += 1
        else:
            target_habit["streak"] = 1

        print(f"{habit_name} marked as done on '{date}'")
        print(f"Current streak '{target_habit['streak']}'")
        self.save_data()

    def show_streak(self):
        print("Streak of a habit")
        print("-"*len("Streak of a habit"))
        self.list_habits()
        habit_name = input("Enter the habit to display the streak : ")
        found = False
        for habit in self.data["habits"]:
            if habit["name"]==habit_name:
                found = True
                target_habit = habit
                print(f"present streak of {habit_name} : {target_habit["streak"]}")

        if not found:
            print(f"There's no habit '{habit_name}'")

    def show_status(self):
        print("Status of a habit")
        print("-"*len("Status of a habit"))
        self.list_habits()
        habit_name = input("Enter the habit : ")
        found = False
        today = date.today().isoformat()
        for habit in self.data["habits"]:
            if habit["name"]==habit_name:
                found=True
                target_habit = habit
                if today in target_habit["logs"]:
                    print(f"{habit_name} on '{today}' : {target_habit['logs'][today]}")
                else:
                    print(f"{habit_name} on '{today}' : not done")
        if not found:
            print(f"There's no habit '{habit_name}'")

    def export_report(self):
        print("Exporting Data")
        print("-"*len("Exporting Data"))
        rows = []
        for habit in self.data["habits"]:
            logs = habit.get("logs", {})
            done_dates = list(logs.keys())

            rows.append([
                habit.get("name", ""),
                habit.get("Created at", ""),
                habit.get("Is active", True),
                len(done_dates),
                max(done_dates) if done_dates else ""
            ])

        with open("exports/Habits_Report.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "created_at", "is_active", "total_done_days", "last_done_date"])
            writer.writerows(rows)

        print(f"Data exported successfully, saved as 'Habits_Report.csv'")
    

class Menu:
    def menu(self):
        print("1. Add habit \n2. Delete habit \n3. Display all habits and info \n4. Mark habit as done (today) \n5. Show streak for a habit \n6. Show today’s status (done/not done) \n7. Export report to CSV \n8. Exit")

    def Choice(self, Hab):
        self.menu()
        while True:
            try:
                choice = int(input("Enter your choice : "))
            except Exception:
                print("Enter a valid number")
                continue

            if choice == 1:
                Hab.add_habit()
            
            elif choice == 2:
                Hab.delete_habit()

            elif choice == 3:
                Hab.display_habits()
                
            elif choice == 4:
                Hab.mark_habit()
            
            elif choice == 5:
                Hab.show_streak()

            elif choice == 6:
                Hab.show_status()

            elif choice == 7:
                Hab.export_report()

            elif choice == 8:
                print("Exiting habit tracker...")
                break

            else:
                print("\nEnter a Valid input")
                self.menu()

            time.sleep(1)
            print()
            self.menu()
            print("What to do next?")
            print()

def Todays_Habits():
        print("Habits done today")
        print("-"*len("Habits done today"))
        today = date.today().isoformat()
        with open("db/Habits.json","r") as f:
            data = json.load(f)
        found = False
        for habit in data["habits"]:
            if today in habit["logs"] and habit["logs"][today] == "done":
                found = True
                for key,value in habit.items():
                    print(f"{key} : {value}")
                time.sleep(0.5)
                print()
        if not found:
            print("No habits marked as done today.")
        time.sleep(0.5)
        print()

def run_habit_tracker():
    print("Welcome to Habit Tracker")
    time.sleep(0.5)
    print("="*len("Welcome to Habit Tracker"))
    time.sleep(0.5)
    print("Select an action to perform")
    Habits = HabitTracker(DB="db/Habits.json")
    menu = Menu()
    menu.Choice(Habits)


if __name__=="__main__":
    run_habit_tracker()
