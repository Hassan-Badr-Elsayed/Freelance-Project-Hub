import re
import json
import datetime as dt

class ValidationError(Exception):
    pass

class ValidationHelper:
    def check_name(self, name):
        if not name or not name.strip():
            raise ValidationError("Name cannot be empty.")
        return name

    def check_password(self, password):
        if type(password) != str or len(password) < 8 or " " in password:
            raise ValidationError("Password must be 8+ chars with uppercase, lowercase, and a digit.")
        
        has_upper = False
        has_lower = False
        has_digit = False
        
        for char in password:
            if char.isupper():
                has_upper = True
            elif char.islower():
                has_lower = True
            elif char.isdigit():
                has_digit = True
                
        if not (has_upper and has_lower and has_digit):
            raise ValidationError("Password must be 8+ chars with uppercase, lowercase, and a digit.")
        return password

    def check_phone(self, phone):
        if type(phone) != str:
            raise ValidationError("Invalid phone number format.")
        phone_pattern = r"^(010|011|012|015)\d{8}$"
        if not re.match(phone_pattern, phone):
            raise ValidationError("Invalid phone number format.")
        return phone

    def check_email(self, email):
        if type(email) != str:
            raise ValidationError("Invalid email format.")
        email_pattern = r"^[^@\s]+@(gmail\.com|yahoo\.com|hotmail\.com|outlook\.com)$"
        if not re.match(email_pattern, email.lower()):
            raise ValidationError("Invalid email format.")
        return email

    def check_account_type(self, account_type):
        if type(account_type) != str or account_type.strip().lower() not in ["freelance", "freelancer", "client"]:
            raise ValidationError("Role must be 'Client' or 'Freelancer'.")
        return account_type

    def check_deadline(self,deadline):
        if type(deadline)!= str or not re.match("^\d{2}-\d{2}-\d{4}$",deadline):
            raise ValidationError("Deadline must be DD-MM-YYYY")
        
        return deadline
    def get_valid_input(self, prompt, validation_function):
        while True:
            try:
                user_input = input(prompt)
                return validation_function(user_input)
            except ValidationError as e:
                print(f"Invalid input: {e} Please try again.\n")

class User:
    id_counter = 1

    def __init__(self, name, email, password, phone_number, role):
        self.id = f"U{User.id_counter:04d}"
        User.id_counter += 1
        self.name = name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.role = role
        
    def display_profile(self):
        pass

class Client(User):
    def __init__(self, name, email, password, phone_number):
        super().__init__(name, email, password, phone_number, "Client")
        
    def display_profile(self):
        return f"[Client] {self.name} | Contact: {self.email} | ID: {self.id}"
    def __str__(self):
        return self.display_profile()

class Freelancer(User):
    def __init__(self, name, email, password, phone_number):
        super().__init__(name, email, password, phone_number, "Freelancer")
        
    def display_profile(self):
        return f"[Freelancer] {self.name} | Contact: {self.email} | ID: {self.id}"
    def __str__(self):
        return self.display_profile()
    
class Project:
    # Create a static variable to keep track of the project ID
    id = 1
    # Constructor
    def __init__(self,title, client, freelancer, status, deadline):
        self.id = f"P{Project.id:04d}"
        Project.id += 1
        self.title = title
        self.client = client
        self.freelancer = freelancer
        self.set_status(status)
        self.set_deadline(deadline)
        
    def __str__(self):
        return f"Project ID: {self.id}\nProject Title: {self.title}\nClient: {self.client}\nFreelancer: {self.freelancer}\nStatus: {self.status}\nDeadline: {self.deadline}"
        
    def set_status(self,status):
        # Check if the status is valid
        if status not in ["open","closed","in progress","cancelled"]:
            raise ValueError(f"Invalid Status:{status}")
        
        self.status = status
    
    def get_status(self):
        return self.status
    
    def set_deadline(self,deadline):
        # Check if the deadline is valid using regex 
        patterns = re.compile("^\d{2}-\d{2}-\d{4}$")
        if not patterns.match(deadline):
            raise ValueError("Deadline must be DD-MM-YYYY")
        self.deadline = deadline
        
    def get_deadline(self):
        return self.deadline
        
    def assign_to_freelancer(self, freelancer):
        # Check if the freelancer is valid and the project is open
        if freelancer.role != "Freelancer":
            raise ValueError("Only freelancers can be assigned to a project.")
        if self.get_status() != "open":
            raise ValueError("Project must be open to assign a freelancer.")
        if self.freelancer is not None:
            raise ValueError("Project already has a freelancer assigned.")
        
        self.freelancer = freelancer
        self.set_status("in progress")
        

class FreelanceManager:
    def __init__(self):
        self.users = {}
        self.projects = {}
        self.validator = ValidationHelper()
        self.load_data()
        
    def register_user(self, name, email, password, phone_number, role):
        if role.lower() == "client":
            new_user = Client(name, email, password, phone_number)
        else:
            new_user = Freelancer(name, email, password, phone_number)
            
        self.users[new_user.id] = new_user
        self.save_data()
        return new_user

    def login(self, user_id, password):
        if user_id in self.users:
            user = self.users[user_id]
            if user.password == password:
                return user
            raise PermissionError("Incorrect password.")
        raise KeyError("User ID not found.")

    def save_data(self, filename="data.json"):
        data_to_save = {}
        users_dict = {}
        
        for user_id, user in self.users.items():
            users_dict[user_id] = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "password": user.password,
                "phone_number": user.phone_number,
                "role": user.role
            }
            
        data_to_save["users"] = users_dict
        ## Save projects data
        projects_dict = {}
        for project_id, project in self.projects.items():
            projects_dict[project_id] = {
                "id": project.id,
                "title": project.title,
                "client_id": project.client.id,
                "freelancer_id": project.freelancer.id if project.freelancer else None,
                "status": project.status,
                "deadline": project.deadline
            }
        data_to_save["projects"] = projects_dict
        
        with open(filename, "w") as file:
            json.dump(data_to_save, file, indent=4)

    def load_data(self, filename="data.json"):
        try:
            with open(filename, "r") as file:
                loaded_data = json.load(file)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            print("Error: Database file contains corrupted JSON.")
        else:
            users_data = loaded_data.get("users", {})
            highest_id = 0
            for user_id, user_info in users_data.items():
                if user_info["role"].lower() == "client":
                    recreated_user = Client(user_info["name"], user_info["email"], user_info["password"], user_info["phone_number"])
                else:
                    recreated_user = Freelancer(user_info["name"], user_info["email"], user_info["password"], user_info["phone_number"])
                
                recreated_user.id = user_info["id"]
                self.users[user_id] = recreated_user
                
                id_num = int(user_info["id"][1:])
                if id_num > highest_id:
                    highest_id = id_num
            User.id_counter = highest_id + 1
            
            ## load projects data
            projects_data = loaded_data.get("projects", {})
            highest_project_id = 0
            for project_id, project_info in projects_data.items():
                client = self.users.get(project_info["client_id"])
                freelancer = self.users.get(project_info["freelancer_id"]) if project_info["freelancer_id"] else None
                recreated_project = Project(project_info["title"], client, freelancer, project_info["status"], project_info["deadline"])
                recreated_project.id = project_info["id"]
                self.projects[project_id] = recreated_project
                
                project_id_num = int(project_info["id"][1:])
                if project_id_num > highest_project_id:
                    highest_project_id = project_id_num
            Project.id = highest_project_id + 1
    
    def create_project(self,title,client_id,deadline):
        # Check if the client ID is valid and corresponds to a Client user
        if client_id not in self.users or self.users[client_id].role != "Client":
            raise ValueError("Invalid client id.")
        # Else create a project object and save it to json
        new_project = Project(title, self.users[client_id], None, "open", deadline)
        self.projects[new_project.id] = new_project
        self.save_data()
        return new_project
    
    def assign_project(self,project_id,freelancer_id):
        if project_id not in self.projects:
            raise ValueError("Invalid Project id")
        if freelancer_id not in self.users or self.users[freelancer_id].role != "Freelancer":
            raise ValueError("Invalid Freelancer id")
        
        # Get this project and freelancer's record
        project = self.projects[project_id]
        freelancer = self.users[freelancer_id]
        # Call Method
        project.assign_to_freelancer(freelancer)
        self.save_data()
        return project
    
    def update_project_status(self,project_id,status):
        if project_id not in self.projects:
            raise ValueError("Invalid project id.")
        project = self.projects[project_id]
        project.set_status(status)
        self.save_data()
        return project
    
    def update_project_deadline(self,project_id,deadline):
        if project_id not in self.projects:
            raise ValueError("Invalid project id.")
        project = self.projects[project_id]
        project.set_deadline(deadline)
        self.save_data()
        return project
    
    def get_projects_for_client(self,client_id):
        if client_id not in self.users or self.users[client_id].role != "Client":
            raise  ValueError("Invalid client id.")
        return list(filter(lambda x: x.client.id == client_id,self.projects.values()))
    
    def get_active_projects(self):
        return list(filter(lambda p: p.status == "in progress", self.projects.values()))
    
    def get_late_projects(self):
        return [
            proj for proj in self.projects.values
            if dt.datetime.strptime(proj.deadline,"%d-%m-%Y")< dt.datetime.now()
            and proj.status not in ["closed","cancelled"]
        ]
        

            
            
        

if __name__ == "__main__":
    manager = FreelanceManager()
    
    while True:
        print("\n--- User Management System ---")
        print("1. Register")
        print("2. Login")
        print("3. Quit")
        choice = input("Select an option (1-3): ")
        
        if choice == "1":
            print("\n--- Registration ---")
            
            name = manager.validator.get_valid_input("Enter name: ", manager.validator.check_name)
            email = manager.validator.get_valid_input("Enter email: ", manager.validator.check_email)
            password = manager.validator.get_valid_input("Enter password: ", manager.validator.check_password)
            phone = manager.validator.get_valid_input("Enter phone number: ", manager.validator.check_phone)
            role = manager.validator.get_valid_input("Enter role (Client/Freelancer): ", manager.validator.check_account_type)
            
            try:
                new_user = manager.register_user(name, email, password, phone, role)
                print(f"\nRegistration successful! Your generated ID is: {new_user.id}")
            except Exception as e:
                print(f"\nUnexpected registration error: {e}")
                
        elif choice == "2":
            while True:
                try:
                    user_id = input("Enter your User ID: ")
                    password = input("Enter your password: ")
                    logged_in_user = manager.login(user_id, password)
                    print(f"\nLogin successful! Welcome back.")
                    print(logged_in_user.display_profile())
                    break
                except (KeyError, PermissionError) as e:
                    print(f"\nInvalid input: {e} Please enter your credentials again.\n")
                except Exception as e:
                    print(f"\nAn unexpected error occurred: {e}")
                    break
            ## Create and Assign project menu
            if logged_in_user is not None:
                while True:
                    print("\n1. Create Project")
                    print("2. Assign Project")
                    print("3. Update Project Status")
                    print("4. Update Project Deadline")
                    print("5. List Client's Projects")
                    print("6. Exit")
                    choice =  input("Enter your choice:")
                    if choice == "1":
                        try:
                            title = input("Enter Project's Title: ")
                            client_id = input("Enter Client's id: ")
                            deadline = manager.validator.get_valid_input("Enter deadline in DD-MM-YYYY Format: ", manager.validator.check_deadline)
                            new_project = manager.create_project(title,client_id,deadline)
                            print(f"\nProject created successfully!\n Project id: {new_project.id}")
                        except ValueError as e:
                            print(f"\nError creating the project: {e}")
                            
                    elif choice  == "2":
                        project_id = input("Enter project ID: ")
                        freelancer_id = input("Enter freelancer ID: ")
                        try:
                            project = manager.assign_project(project_id, freelancer_id)
                            print(f"\nProject {project.id} assigned successfully!")
                        except ValueError as e:
                            print(f"\nError assigning project: {e}")
                            
                    elif choice == "3":
                        project_id = input("Enter project ID: ")
                        new_status = input("Enter new status (open/in progress/closed/cancelled): ")
                        try:
                            project = manager.update_project_status(project_id, new_status)
                            print(f"\nProject {project.id} status updated to '{project.status}'.")
                        except ValueError as e:
                            print(f"\nError updating status: {e}")
                            
                    elif choice == "4":
                        project_id = input("Enter project ID: ")
                        new_deadline = input("Enter new deadline(DD-MM-YYYY): ")
                        try:
                            project = manager.update_project_deadline(project_id, new_deadline)
                            print(f"\nProject {project.id} deadline updated to '{project.deadline}'.")
                        except ValueError as e:
                            print(f"\nError updating deadline: {e}")
                            
                    elif choice == "5":
                        client_id = input("Enter client ID: ")
                        try:
                            client_projects = manager.get_projects_for_client(client_id)
                            if not client_projects:
                                print("This client has no projects.")
                            for project in client_projects:
                                print(project)
                                print("-" * 30)
                        except ValueError as e:
                            print(f"\nError: {e}")
                            
                    elif choice == "6":
                        break
                    else:
                        print("Please choose an option between 1-4.")
                                                                                    
                                                        
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please enter 1, 2, or 3.")