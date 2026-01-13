#NOTES TRACKER

import time
import os
import json
import csv
from datetime import date

class NotesTracker:
    def __init__(self,DB="db/Notes.json"):
        if not os.path.exists(DB):
            with open("db/Notes.json","w") as f:
                json.dump(
                {
                  "notes": []
                },f,
                indent=4
                )
        self.load_data()

    def load_data(self):
        with open("db/Notes.json","r") as f:
            self.data = json.load(f)

    def save_data(self):
        with open("db/Notes.json","w") as f:
            json.dump(self.data,f,indent=4)

    def list_notes(self):
        print("List of notes")
        print("."*len("List of notes"))
        i=1
        for note in self.data["notes"]:
            if not note["archived"] and note["pinned"]:
                print(f"{i}. {note["title"]}")
                i+=1
        for note in self.data["notes"]:
            if not note["archived"] and not note["pinned"]:
                print(f"{i}. {note["title"]}")
                i+=1
        
    def add_note(self):
        print("Adding Note")
        print("-"*len("Adding Note"))
        title = input("Enter the title of note : ")
        content = input("Enter the content : ")
        created_at = date.today().isoformat()
        updated_at = "None"
        tags = []
        no_of_tags = int(input("Enter no of tags for the notes : "))
        for i in range(no_of_tags):
            tag = input(f"Enter tag {i+1} : ")
            tags.append(tag)

        extra_notes_choice = input("Any extra notes? (Y/N) : ").capitalize()
        if extra_notes_choice == "Y":
            extra_notes = input("Extra notes : ")
        elif extra_notes_choice == "N":
            extra_notes = ""
        
        pin_choice = input("Pin the notes? (Y/N) : ").capitalize()
        if pin_choice == "Y":
            pinned=True
        elif pin_choice == "N":
            pinned=False

        archive_choice = input("Archive the notes? (Y/N) : ").capitalize()
        if archive_choice == "Y":
            archived = True
        elif archive_choice == "N":
            archived = False
            
        note = {
                "title":title,
                "content":content,
                "tags":tags,
                "created_at":created_at,
                "updated_at":updated_at,
                "extra_notes":extra_notes,
                "pinned":pinned,
                "archived":archived
                }  
        self.data["notes"].append(note)  
        self.save_data()
        print("Added Notes")    
    
    def delete_note(self):
        print("Deleteing Note")
        print("-"*len("Deleteing Note"))
        print("List of notes")
        print("."*len("List of notes"))
        i=1
        for note in self.data["notes"]:
            print(f"{i}. {note["title"]}")
            i+=1
        title = input("Enter the title of note to delete : ")
        found = False
        for note in self.data["notes"]:
            if note["title"] == title:
                found = True
                target_note = note
                self.data["notes"].remove(target_note)

        print(f"Removed note : {title}")
        if not found:
            print(f"Note '{title}' not found")
        self.save_data()

    def display_note_info(self):
        print("Displaying Notes info")
        print("-"*len("Displaying Notes info"))
        self.list_notes()
        title = input("Enter title of note to display info : ")
        found = False 
        for note in self.data["notes"]:
            if note["title"] == title and not note["archived"]:
                found = True
                target_note = note
                print(f"Title : {target_note["title"]}")
                print(f"Content : {target_note["content"]}")
                print("Tags : ", ", ".join(target_note["tags"]))
                print(f"Extra Notes : {target_note["extra_notes"]}")
                print(f"Created at : {target_note["created_at"]}")
                print(f"Last updated at : {target_note["updated_at"]}")
                print(f"Pinned : {"Yes" if target_note["pinned"] else "No"}")

         
        
        if not found:
            print(f"Note '{title}' not found")

    def edit_note(self):
        print("Editing Note")
        print("-"*len("Editing Note"))
        self.list_notes()
        title = input("Enter note title to edit it : ")
        edits = ["1. Title","2. Content","3. Extra notes"]
        print("You can only edit : ",*edits)
        edit_choice = int(input("Enter your choice : "))
        found = False
        for note in self.data["notes"]:
            if note["title"] == title and not note["archived"]:
                found = True
                target_note = note
                if edit_choice == 1:
                    updated_title = input("Enter the updated title : ")
                    target_note["title"]=updated_title
                    target_note["updated_at"] = date.today().isoformat()
                    print(f"Title updated to '{updated_title}'")
                elif edit_choice == 2:
                    updated_content = input("Enter updated content : ")
                    target_note["content"]=updated_content
                    target_note["updated_at"] = date.today().isoformat()
                    print(f"Title updated to '{updated_content}'")
                elif edit_choice == 3:
                    updated_notes = input("Enter the updated extra notes : ")
                    target_note["extra_notes"]=updated_notes
                    target_note["updated_at"] = date.today().isoformat()
                    print(f"Title updated to '{updated_notes}'")
            
        if not found:
            print(f"Note '{title}' not found")
        self.save_data()

    def search_note(self):
        print("Searching Note")
        print("-"*len("Searching Note"))
        detail = input("Enter a tag/title to find the notes : ")
        found = False
        for note in self.data["notes"]:
            if (detail in note["tags"] or detail == note["title"] or detail in note["title"]) and not note["archived"]:
                found = True
                target_note = note
                print(f"Title : {target_note["title"]}")
                print("Tags : ", ", ".join(target_note["tags"]))
                print(f"Content : {target_note["content"]}")
                print(f"Created at : {target_note["created_at"]}")
                print(f"last updated at : {target_note["updated_at"]}")
            
        if not found:
            print(f"Nothing found related to '{detail}'")
        
    def pin_archive_notes(self,choice):
        if choice == 7:
            print("Pin/Upin notes")
            print("-"*len("Pin/Upin notes"))
            title = input("Enter title of note : ")
            found = False
            for note in self.data["notes"]:
                if note["title"]==title:
                    found = True
                    target_note = note
                    print(f"'{target_note["title"]}' is {"pinned" if target_note["pinned"] else "not pinned"}")
                    if target_note["pinned"]:
                        unpin_choice = input(f"Unpin '{target_note["title"]}'? (Y/N) : ").capitalize()
                        if unpin_choice == "Y":
                            target_note["pinned"]=False
                            
                    else:
                        pin_choice = input(f"Pin '{target_note["title"]}'? (Y/N) : ").capitalize()
                        if pin_choice == "Y":
                            target_note["pinned"]=True
                            
            
            if not found:
                print(f"Note '{title}' not found")

        elif choice == 8:
            print("Archive/Unarchive notes")
            print("-"*len("Archive/Unarchive notes"))
            title = input("Enter title of note : ")
            found = False
            for note in self.data["notes"]:
                if note["title"]==title:
                    found = True
                    target_note = note
                    print(f"'{target_note["title"]}' is {"archived" if target_note["archived"] else "not archived"}")
                    if target_note["archived"]:
                        unarchive_choice = input(f"Unarchive '{target_note["title"]}'? (Y/N) : ").capitalize()
                        if unarchive_choice == "Y":
                            target_note["archived"]=False
                            
                    else:
                        archive_choice = input(f"archive '{target_note["title"]}'? (Y/N) : ").capitalize()
                        if archive_choice == "Y":
                            target_note["archived"]=True
                            
            
            if not found:
                print(f"Note '{title}' not found")
        
        self.save_data()

    def export_report(self):
        print("Exporting Data")
        print("-"*len("Exporting Data"))
        rows = []
        for note in self.data["notes"]:
            tags = ",".join(note.get("tags",[]))
            rows.append([
                note.get("title", ""),
                tags,
                note.get("created_at", ""),
                note.get("updated_at",""),
                note.get("pinned",False),
                note.get("archived",False)
            ])

        with open("Notes_Report.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name","tags","created_at","updated_at","pinned","archived"])
            writer.writerows(rows)

        print(f"Data exported successfully, saved as 'Notes_Report.csv'")
        

class Menu:
    def menu(self):
        print("1. Add note \n2. Delete habit \n3. List notes \n4. View note \n5. Search note \n6. Edit note \n7. Pin/Unpin note \n8. Archive/Unarchive \n9. Export CSV report \n10. Exit")

    def Choice(self, note):
        self.menu()
        while True:
            try:
                choice = int(input("Enter your choice : "))
            except Exception:
                print("Enter a valid number")
                continue

            if choice == 1:
                note.add_note()
            
            elif choice == 2:
                note.delete_note()

            elif choice == 3:
                note.list_notes()
                
            elif choice == 4:
                note.display_note_info()
            
            elif choice == 5:
                note.search_note()

            elif choice == 6:
                note.edit_note()

            elif choice == 7 or choice == 8:
                note.pin_archive_notes(choice)

            elif choice == 9:
                note.export_report()

            elif choice == 10:
                print("Exiting notes tracker...")
                break

            else:
                print("\nEnter a Valid input")
                self.menu()

            time.sleep(1)
            print()
            self.menu()
            print("What to do next?")
            print()

def run_note_tracker():
    print("Welcome to Notes Tracker")
    time.sleep(0.5)
    print("="*len("Welcome to Notes Tracker"))
    time.sleep(0.5)
    print("Select an action to perform")
    Notes = NotesTracker(DB="db/Notes.json")
    menu = Menu()
    menu.Choice(Notes)

if __name__=="__main__":
    run_note_tracker()