#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from modules import *

class Cli:
    def __init__(self):
        self.engine = create_engine("sqlite:///lib/family.db")
        self.session = Session(self.engine)
        self.create_database()        
        self.welcome()
        self.login_and_get_user_id()
        
    def create_database(self):
        Base.metadata.create_all(self.engine)

    def welcome(self):
        print("""
~~~ Welcome to Kinship Terminal!!~~~""")

    def login_and_get_user_id(self):
        while True:
            
            print(' ')
            print(' ')
            print('Select from the two options below:')
            print(' ')
            print('1. Visitor')
            print('2. User')
            print(' ')
            

            type_user = input('Which of the options above?: ')
            if type_user == '1':
                self.create_user()
                             
            elif type_user == '2':  # Compare with a string, not an integer
                print(' ')
                first_name = input("Enter your first name: ")
                last_name = input("Enter your last name: ")

                user = self.session.query(User).filter(
                    User.first_name == first_name,
                    User.last_name == last_name
                ).first()

                if user:
                    print(' ')
                    print(f"User found in the database: {user.id} | {user.first_name}")
                    print(' ')
                    print(' ')
                    print(f"Welcome, {user.first_name } {user.last_name}!")
                    name = f'{user.first_name} {user.last_name}'
                    self.starter(user.id, name)
                    break  # Exit the loop if login is successful
                else:
                    print("Login failed. Please try again.")
                
            else:
                print('Wrong input! Pick one of the 2 options.')
 
                    
    def starter(self, user_id, name='' ):
        
        while True:
            
            print(" ")
            print("Please select from the following options:")
            print(" ")
            print("Press V to view family.")
            print("Press A to add people")
            print("Press C to connect newly added family members to others.")
            print("Press U to update the information about a family member.")
            print("Press D to delete a person.")
            print("Press G to generate family tree.")
            print(" ")
            print("Press Q to quit.")
            print(" ")
            user_choice = input("What would you like to do next? ")
            print(" ")

            if user_choice == "V" or user_choice == "v":
                Cli.view_family(self, user_choice, user_id)
            elif user_choice == "A" or user_choice == "a":
                Cli.add_family(self, user_choice, user_id)
            elif user_choice == "C" or user_choice == "c":
                Cli.create_connection(self, user_choice, user_id)
            elif user_choice == "U" or user_choice == "u":
                Cli.update_status(self, user_choice, user_id)
            elif user_choice == "D" or user_choice == "d":
                Cli.delete_individual(self, user_choice, user_id)
            elif user_choice == "G" or user_choice == "g":
                Cli.generate_tree(self, user_choice, user_id)
            elif user_choice == "Q":
                exit()
            else:
                print("Invalid option entered. Please select from the list of options or press Q to exit.")

            

    def view_family(self, user_choice, user_id):
        if user_choice:
            query = self.session.query(Person).filter(Person.user_id == user_id).all()

            if query:
                print(' ')
                print('Your Relatives/Family')
                print(' ')

                for i in query:
                     print(f'{i.id} |  {i.first_name} {i.last_name }')
                print(' ')
                print(' ')

                main = input('Press any key to go back to the main menu: ')

                if main :
                        self.starter(user_id)
            
                     
            else:
                print('No family memebers added at the moment.')
                print(' ')
                
                answer = input("Press Any Key To Go Back To main Menu")

               
    def add_family(self, user_choice, user_id):
        if user_choice:
            print(" ")
            print("Add a New Person")
            print(" ")
            first_name = input("Enter First Name: ")
            last_name = input("Enter Last Name: ")
            relationship = input('How are you related? ')

        # Create a new Person instance
            new_person = Person(first_name=first_name, last_name=last_name, user_id=user_id, user_relashionship=relationship)

        # Add the new person to the database
            self.session.add(new_person)
            self.session.commit()
            print(' ')
            print(f"{new_person.first_name} {new_person.last_name} has been added!")
            print(' ')
  
                
        

    def create_connection(self, user_choice, user_id):
        print(" ")
        print("Create a New Connection")
        print(" ")

        family_members = self.session.query(Person).filter(Person.user_id == user_id).all()
        if not family_members:
            print(' ')
            print("You need to add family members first.")
            print(' ')
            return

        print("Select the individuals to connect:")
        print(' ')
        for member in family_members:
            print(' ')
            print(f"{member.id}: {member.first_name} {member.last_name}")
            print(' ')
            
        person1_id = input("Enter the ID of the first person: ")
        print(' ')
        person2_id = input("Enter the ID of the second person: ")

        person1 = self.session.query(Person).filter(Person.id == person1_id, Person.user_id == user_id).first()
        print(' ')
        person2 = self.session.query(Person).filter(Person.id == person2_id, Person.user_id == user_id).first()

        if not person1 or not person2:
            print("Invalid person IDs. Please select valid family members.")
        
        print(' ')
        print('What relationship out of these 3 options do they share?')
        
        print('1. Parent')
        print('2. Spouses')
        print('3. Sibling')
        print(' ')
        
        relationship_type = input("Enter either one of those options: ")
        
        if relationship_type == '1':
            new_connection = connections.insert().values(
            individual1_id=person1.id,
            individual2_id=person2.id,
            relationship_id= relationship_type,
            users_id= user_id
        )
            self.session.execute(new_connection)
            self.session.commit()
            
            print(' ')
            print(f"Connection created between {person1.first_name} and {person2.first_name}: {relationship_type}") 
        elif relationship_type == '2':
               
            new_connection = connections.insert().values(
            individual1_id=person1.id,
            individual2_id=person2.id,
            relationship_id= relationship_type,
            users_id= user_id
        )

            self.session.execute(new_connection)
            self.session.commit()
            print(' ')
            print(f"Connection created between {person1.first_name} and {person2.first_name}: {relationship_type}") 
        elif relationship_type == '3':
            new_connection = connections.insert().values(
            individual1_id=person1.id,
            individual2_id=person2.id,
            relationship_id= relationship_type,
            users_id= user_id
        )
            self.session.execute(new_connection)
            self.session.commit()
            
            print(' ')
            print(f"Connection created between {person1.first_name} and {person2.first_name}: {relationship_type}")
        else:
            print('Not supported, only pick the listed options.')


    def update_status(self, user_choice, user_id):
        print(' ')
        print("Update Family Member Information")
        print(' ')
        # Display the list of family members
        family_members = self.session.query(Person).filter(Person.user_id == user_id).all()

        if not family_members:
            print(' ')
            print("No family members found.")
            print(' ')
            return

        print(' ')
        print("Select the individual to update:")
        print(' ')
        for member in family_members:
            print(' ')
            print(f"{member.id}: {member.first_name} {member.last_name} > {member.user_relashionship}")
            print(' ')
        person_id = input("Enter the ID of the person you want to update: ")

        person_to_update = self.session.query(Person).filter(
            Person.id == person_id,
            Person.user_id == user_id
        ).first()

        if not person_to_update:
            print(' ')
            print("Person not found in the database.")
            print(' ')
        else:
            print(f"Selected person: {person_to_update.first_name} {person_to_update.last_name}")
            print(' ')
            print("What would you like to update?")
            print("1. First Name")
            print("2. Last Name")
            print("3. Status")
            print(' ')
            update_option = input("Enter the option number: ")

            if update_option == "1":
                new_first_name = input("Enter the new first name: ")
                person_to_update.first_name = new_first_name
            elif update_option == "2":
                new_last_name = input("Enter the new last name: ")
                person_to_update.last_name = new_last_name
            elif update_option == "3":
                new_status = input("Enter the new status: ")
                person_to_update.user_relashionship = new_status
            else:
                print("Invalid option. No updates performed.")

            self.session.commit()
            print(' ')
            print(f"Information updated for {person_to_update.first_name} {person_to_update.last_name}.")
    
    
    def delete_individual(self, user_choice, user_id):
        while user_choice:
            print(' ')
            print('Delete Family Member')
        
            query = self.session.query(Person).filter(Person.user_id == user_id).all()

            if query:
                print(' ')
                print('Your Relatives/Family')
                print(' ')

                for i in query:
                     print(f'{i.id}   |  {i.first_name} {i.last_name } > {i.user_relashionship}')
                print(' ')
                print(' ')
        
                print(' ')
            else:
                print(' ')
                print('No one to delete.')
                print(' ')
                
            
            person_id = input('Pick the Id of the person you want to delete: ')
            
        
        
            person_to_delete = self.session.query(Person).filter(Person.id == person_id).first()

            if not person_to_delete:
        # Handle the case where the person does not exist
                print(' ')
                print("Person not found in the database.")
                        
            else:
        # Delete the person from the database
                try:
                    self.session.delete(person_to_delete)
                    connections_to_delete = connections.delete().where(
                    (connections.c.individual1_id == person_to_delete.id) |
                    (connections.c.individual2_id == person_to_delete.id)
                    )
                    self.session.execute(connections_to_delete)
                    self.session.commit()
                    print(' ')
                    print(f"Successfully deleted person {person_to_delete.first_name} {person_to_delete.last_name}.")
                    print(' ')
                except Exception as e:
                    self.session.rollback()
                    print(f"Error deleting person: {str(e)}")
                    print(' ')
                go_back = input("Press any key to go back to the main menu or 'Q' to quit: ")
                if go_back.lower() == 'q':
                    exit()
                else:
                    self.starter(user_id)

    def create_user(self):
        print(" ")
        print("Create a New User")
        print(" ")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        new_user = User(first_name=first_name, last_name=last_name)
        existing_user = self.session.query(User).filter(
            User.first_name == new_user.first_name,
            User.last_name == new_user.last_name
         ).first()
        if existing_user:
                 print('This user already exists!')
        else:
                 self.session.add(new_user)
                 self.session.commit()
                 print(f"User {new_user.id}:{new_user.first_name} {new_user.last_name} has been created!")
                 self.starter(new_user.id)
    
    
    def generate_tree(self, user_choice, user_id):
        print("Generating family tree is not implemented yet.")
    
        

if __name__ == '__main__':
    Cli()