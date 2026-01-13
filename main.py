import time
from trackers.Expense_Tracker import run_expense_tracker
from trackers.Habit_Tracker import run_habit_tracker
from trackers.Notes_Tracker import run_note_tracker

print("Welcome to Psycho Notion lite")
time.sleep(0.5)
print("="*len("Welcome to Psycho Notion lite"))
time.sleep(0.5)
print("Select an action to perform")

class NotionLite:
    def menu(self):
        print("1. Expense Tracker \n2. Habit Tracker \n3. Notes Tracker \n4. Exit")

    def Choice(self):
        self.menu()
        while True:
            try:
                choice = int(input("Enter your choice : "))
            except Exception:
                print("Enter a valid numer")
                continue
            if choice == 1:
                run_expense_tracker()
            elif choice == 2:
                run_habit_tracker()
            elif choice == 3:
                run_note_tracker()
            elif choice == 4:
                print("Exiting...")
                break
            else:
                print("\nEnter a Valid input")
                self.menu()

            time.sleep(1)
            print()
            print("Returned to Psycho Notion Lite")
            self.menu()
            print("What to do next?")
            print()

Notion = NotionLite()
Notion.Choice()


