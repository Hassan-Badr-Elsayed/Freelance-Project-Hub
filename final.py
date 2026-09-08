import re
import json
import datetime as dt
from functools import reduce

# Custom Exception across validator
class ValidationError(Exception):
    pass

class ValidationHelper:
    def check_name(self, name):
        # Check empty strings or whitespace strings
        if not name or not name.strip():
            raise ValidationError("Name cannot be empty.")
        return name

    def check_password(self, password):
        # Check if it is a string , long enough, and no spaces
        if type(password) != str or len(password) < 8 or " " in password:
            raise ValidationError("Password must be 8+ chars with uppercase, lowercase, and a digit.")
        # Initialize validation flags
        has_upper = False
        has_lower = False
        has_digit = False
       # Loop through each char to check categories
        for char in password:
            if char.isupper():
                has_upper = True
            elif char.islower():
                has_lower = True
            elif char.isdigit():
                has_digit = True
       # Must contain all three categories
        if not (has_upper and has_lower and has_digit):
            raise ValidationError("Password must be 8+ chars with uppercase, lowercase, and a digit.")
        return password

    def check_phone(self, phone):
        if type(phone) != str:
            raise ValidationError("Invalid phone number format.")
        # Common mobile prefixes 
        phone_pattern = r"^(010|011|012|015)\d{8}$"
        if not re.match(phone_pattern, phone):
            raise ValidationError("Invalid phone number format.")
        return phone

    def check_email(self, email):
        if type(email) != str:
            raise ValidationError("Invalid email format.")
         # Common email providers
        email_pattern = r"^\S+@\S+\.\S+$"
        if not re.match(email_pattern, email.lower()):
            raise ValidationError("Invalid email format.")
        return email

    def check_account_type(self, account_type):
         # Deadline must look like DD-MM-YYYY
        if type(account_type) != str or account_type.strip().lower() not in ["freelancer", "client"]:
            raise ValidationError("Role must be 'Client' or 'Freelancer'.")
        return account_type

    def check_deadline(self,deadline):
        if type(deadline)!= str or not re.match(r"^\d{2}-\d{2}-\d{4}$",deadline):
            raise ValidationError("Deadline must be DD-MM-YYYY")

        return deadline
    def get_valid_input(self, prompt, validation_function):
        # Keep asking until given validation function accepts input
        while True:
            try:
                user_input = input(prompt)
                return validation_function(user_input)
            except ValidationError as e:
                print(f"Invalid input: {e} Please try again.\n")



class User:
    # Shared counter across users
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
         # Role is fixed to "Client"
        super().__init__(name, email, password, phone_number, "Client")

    def display_profile(self):
        return f"[Client] {self.name} | Contact: {self.email} | ID: {self.id}"
    def __str__(self):
        return self.display_profile()

class Freelancer(User):
    def __init__(self, name, email, password, phone_number):
         # Role is fixed to "Freelancer"
        super().__init__(name, email, password, phone_number, "Freelancer")

    def display_profile(self):
        return f"[Freelancer] {self.name} | Contact: {self.email} | ID: {self.id}"
    def __str__(self):
        return self.display_profile()
    
class Admin(User):
    def __init__(self, name, email, password, phone_number):
        # Role is fixed to "Admin"
        super().__init__(name, email, password, phone_number, "Admin")

    def display_profile(self):
        return f"[Admin] {self.name} | Contact: {self.email} | ID: {self.id}"
    
    def __str__(self):
        return self.display_profile()

class Project:
    # Fixed budgets allowed for invoice
    budgets = [1000,2500,5000,10000,20000]
    # Create a static variable to keep track of the project ID
    id = 1
    # Constructor
    def __init__(self,title, client, freelancer, status, deadline,budget):
        self.id = f"P{Project.id:04d}"
        Project.id += 1
        self.title = title
        self.client = client
        self.freelancer = freelancer
         # Use setters on initial creation
        self.set_status(status)
        self.set_deadline(deadline)
        self.set_budget(budget)
        self.milestones = []
        self.milestone_history = []

    def __str__(self):
        return f"Project ID: {self.id}\nProject Title: {self.title}\nClient: {self.client}\nFreelancer: {self.freelancer}\nStatus: {self.status}\nDeadline: {self.deadline}\nBudget: {self.budget}"

    def set_status(self,status):
        # Check if the status is valid
        if status not in ["open","closed","in progress","cancelled"]:
            raise ValueError(f"Invalid Status:{status}")

        self.status = status

    def get_status(self):
        return self.status

    def set_deadline(self,deadline):
        # Check if the deadline is valid using regex
        patterns = re.compile(r"^\d{2}-\d{2}-\d{4}$")
        if not patterns.match(deadline):
            raise ValueError("Deadline must be DD-MM-YYYY")
        self.deadline = deadline

    def get_deadline(self):
        return self.deadline
    
    def set_budget(self,budget):
        if budget not in Project.budgets:
            raise ValueError("Invalid project budget.")
        self.budget = budget
            
    def assign_to_freelancer(self, freelancer):
        # Check if the freelancer is valid and the project is open
        if freelancer.role != "Freelancer":
            raise ValueError("Only freelancers can be assigned to a project.")
        if self.get_status() != "open":
            raise ValueError("Project must be open to assign a freelancer.")
        if self.freelancer is not None:
            raise ValueError("Project already has a freelancer assigned.")
        
         # Assign a freelance and update state
        self.freelancer = freelancer
        self.set_status("in progress")
    def add_milestone(self, name):
        milestone = {
            "name": name,
            "status": "pending"
        }
        self.milestones.append(milestone)
    def update_milestone(self, milestone_name, new_status):
        if new_status not in ["pending", "in progress", "completed"]:
            raise ValueError(
                "Invalid milestone status. Use pending, in progress, or completed."
            )
        for milestone in self.milestones:
            if milestone["name"] == milestone_name:
                old_status = milestone["status"]
                milestone["status"] = new_status
                milestone_record = {
                    "milestone": milestone_name,
                    "old_status": old_status,
                    "new_status": new_status,
                    "date": dt.datetime.now().strftime("%d-%m-%Y")
                }
                self.milestone_history.append(milestone_record)
                return

        raise ValueError("Milestone not found.")

    def show_milestone_history(self):
        if not self.milestone_history:
            print("No milestones found.")
            return

        for milestone in self.milestone_history:
            print(
                f"Milestone: {milestone['milestone']}\n"
                f" status: {milestone['new_status']}\n"
                f"Date: {milestone['date']}"
            )


def create_commission_rule(rate):
    total_commission_collected = 0
    
    def commission_rule(amount):
        nonlocal total_commission_collected
        calculated_commission = amount * rate
        total_commission_collected += calculated_commission
        return calculated_commission
        
    return commission_rule

# Every invoice uses a fixed 10% commission rate
commission_rule = create_commission_rule(0.10)

# Custom Exception handler
class InvalidInvoiceAmount(Exception):
    pass

class Invoice:
    # Shared static counter
    invoice_counter = 0
    
    def __init__(self,amount,project_id=None):
         # Validate amount 
        if amount not in Project.budgets:
            raise InvalidInvoiceAmount("Invalid invoice amount.")
        self.amount = amount
        self.project_id = project_id
        Invoice.invoice_counter += 1
        self.code = f"INV{Invoice.invoice_counter:04d}"
        self.status = "Unpaid"
        self.commission = 0
    
    def code_validation(self):
         # Check invoice code match expected format
        regex = re.compile(r'^INV\d{4}$')
        if not re.match(regex, self.code):
            raise ValueError("Invalid invoice code.")

        return True

    def calc_commission(self):
        # Apply 10% commission rule
        self.commission = commission_rule(self.amount)
        
    def mark_as_paid(self):
        self.status = "Paid"
    
    def export_to_txt(self):
        # Create a filename with invoice code txt
        filename = f"{self.code}.txt"
        with open(filename,"w") as file:
            file.write(f"INVOICE RECEIPT: {self.code}\n")
            file.write("=" * 35 + "\n")
            file.write(f"Project ID : {self.project_id}\n")
            file.write(f"Gross Amount : ${self.amount}\n")
            file.write(f"Commission : ${self.commission}\n")
            file.write(f"Net Earnings : ${self.amount - self.commission}\n")
            file.write(f"Status : {self.status}\n")
            file.write("=" * 35 + "\n")
        print(f"Exported receipt to {filename}")
        
    

class Report:
     # Report class to generate a summary of earnings , late projects , and active projects
    def __init__(self):
        self.earnings = 0
        self.late_projects = []
        self.active_work = []
        
    def calc_earnings(self,invoices):
        # Keep only paid invoices
        paid_invoices = filter(lambda invoice: invoice.status == "Paid", invoices)
        # And then Get sum for each
        self.earnings = reduce(lambda total,invoice: total + (invoice.amount - invoice.commission), paid_invoices,0)
        return self.earnings
    
    def get_late_projects(self,projects):
        # Project is late if deadline has passed and not cancelled or closed
        self.late_projects = list(filter(lambda project: dt.datetime.strptime(project.deadline,"%d-%m-%Y")< dt.datetime.now() and project.status not in ["closed","cancelled"], projects))
        return self.late_projects
    
    def get_active_work(self,projects):
        # Project is active if it is in "In progress" state
        self.active_work = list(filter(lambda project: project.status == "in progress", projects))
        return self.active_work
    
    def __str__(self):
        return f"Payment Report\nEarning : {self.earnings}\nLateProjects : {len(self.late_projects)}\nActiveWork : {len(self.active_work)}"
    
class FreelanceManager:
    def __init__(self):
        self.users = {}
        self.projects = {}
        self.invoices={}
        self.validator = ValidationHelper()
        # Load data on startup
        self.load_data()

    def register_user(self, name, email, password, phone_number, role):
        # Create right subclass based on chosen role
        if role.lower() == "client":
            new_user = Client(name, email, password, phone_number)
        elif role.lower() == "freelancer":
            new_user = Freelancer(name, email, password, phone_number)
        elif role.lower() == "admin":
            new_user = Admin(name, email, password, phone_number)
        else:
            raise ValueError("Invalid Role")
        
        self.users[new_user.id] = new_user
        self.save_data()
        return new_user

    def login(self, user_id, password):
        # Check against user id and password
        if user_id in self.users:
            user = self.users[user_id]
            if user.password == password:
                return user
            raise PermissionError("Incorrect password.")
        raise KeyError("User ID not found.")
    
    
    def save_data(self, filename="data.json"):
        data_to_save = {}
        users_dict = {}
         # Convert objects to dicts for json to handle
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
                "deadline": project.deadline,
                "budget": project.budget,
                "milestones":project.milestones,
                "milestone_history":project.milestone_history,
            }
        data_to_save["projects"] = projects_dict
        
        # Save invoices data

        invoices_dict = {}
        for invoice_code, invoice in self.invoices.items():
            invoices_dict[invoice_code] = {
                "code": invoice.code,
                "amount": invoice.amount,
                "project_id": invoice.project_id,
                "status": invoice.status,
                "commission": invoice.commission
            }
        
        data_to_save["invoices"] = invoices_dict

        with open(filename, "w") as file:
            json.dump(data_to_save, file, indent=4)

    def load_data(self, filename="data.json"):
        try:
            with open(filename, "r") as file:
                loaded_data = json.load(file)
        except FileNotFoundError:
             # If file doesn't exist then start with an empty state
            pass
        except json.JSONDecodeError:
            print("Error: Database file contains corrupted JSON.")
        else:
            users_data = loaded_data.get("users", {})
            highest_id = 0
            for user_id, user_info in users_data.items():
                if user_info["role"].lower() == "client":
                    recreated_user = Client(user_info["name"], user_info["email"], user_info["password"], user_info["phone_number"])
                elif user_info["role"].lower() == "freelancer":
                    recreated_user = Freelancer(user_info["name"], user_info["email"], user_info["password"], user_info["phone_number"])
                elif user_info["role"].lower() == "admin":
                    recreated_user = Admin(user_info["name"], user_info["email"], user_info["password"], user_info["phone_number"])

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
                recreated_project = Project(project_info["title"], client, freelancer, project_info["status"], project_info["deadline"],project_info.get("budget", 1000))
                recreated_project.id = project_info["id"]
                recreated_project.milestones = project_info.get("milestones", [])
                recreated_project.milestone_history = project_info.get("milestone_history", [])

                self.projects[project_id] = recreated_project

                project_id_num = int(project_info["id"][1:])
                if project_id_num > highest_project_id:
                    highest_project_id = project_id_num
            Project.id = highest_project_id + 1
            
            # Load invoices data
            invoices_data = loaded_data.get("invoices", {})
            highest_invoice_id = 0

            for invoice_code, invoice_info in invoices_data.items():
                invoice = Invoice(
                    invoice_info["amount"],
                    invoice_info["project_id"]
                )

                invoice.code = invoice_info["code"]
                invoice.status = invoice_info["status"]
                invoice.commission = invoice_info["commission"]

                self.invoices[invoice_code] = invoice

                invoice_id_num = int(invoice.code[3:])

                if invoice_id_num > highest_invoice_id:
                    highest_invoice_id = invoice_id_num

            Invoice.invoice_counter = highest_invoice_id

    def create_project(self,title,client_id,deadline,budget):
        # Check if the client ID is valid and corresponds to a Client user
        if client_id not in self.users or self.users[client_id].role != "Client":
            raise ValueError("Invalid client id.")
        # Else create a project object and save it to json
        new_project = Project(title, self.users[client_id], None, "open", deadline,budget)
        self.projects[new_project.id] = new_project
        self.save_data()
        return new_project

    def assign_project(self,project_id,freelancer_id):
        # Validate both ids

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

    def generate_invoice(self):
        project_id = input("Enter Project ID: ")

        if project_id not in self.projects:
            print("Project ID not found.")
            return

        project = self.projects[project_id]

        print("\nAvailable Invoice Amounts:")
        for i, amount in enumerate(Project.budgets, start=1):
            print(f"{i}. ${amount}")

        try:
            choice = int(input("Choose invoice amount: "))

            if choice < 1 or choice > len(Project.budgets):
                print("Invalid choice.")
                return

            amount = Project.budgets[choice - 1]

            invoice = Invoice(amount, project.id)

            invoice.calc_commission()
            invoice.code_validation()

            self.invoices[invoice.code] = invoice
            self.save_data()

            print("\nInvoice generated successfully!")
            print(f"Invoice Code: {invoice.code}")
            print(f"Project ID: {invoice.project_id}")
            print(f"Amount: ${invoice.amount}")
            print(f"Commission: ${invoice.commission}")
            print(f"Status: {invoice.status}")

        except InvalidInvoiceAmount:
            print("Please choose a valid invoice amount.")
        except ValueError as e:
            print(f"Invoice validation error: {e}")
        except Exception as e:
            print(f"Error generating invoice: {e}")
    
    def mark_invoice_as_paid(self):
            invoice_code = input("Enter Invoice Code: ")
    
            if invoice_code not in self.invoices:
                print("Invoice Code not found.")
                return
    
            invoice = self.invoices[invoice_code]
    
            if invoice.status == "Paid":
                print("Invoice is already paid.")
                return
    
            invoice.mark_as_paid()
            self.save_data()
    
            print(f"Invoice {invoice.code} marked as Paid.")
    def display_invoices(self):
            if not self.invoices:
                print("No invoices found.")
                return
    
            print("Invoices ")
    
            for invoice in self.invoices.values():
                print(f"Invoice Code: {invoice.code}")
                print(f"Project ID: {invoice.project_id}")
                print(f"Amount: {invoice.amount}")
                print(f"Commission: {invoice.commission}")
                print(f"Status: {invoice.status}")
    
    def delete_project_interactive(self, current_user):
        if current_user.role != "Admin":
            print("\nPermission Denied: Only Admins can delete projects.")
            return

        project_id = input("Enter project ID to delete: ")
        
        if project_id not in self.projects:
            print("\nError: Invalid Project ID.")
            return
            
        confirm = input(f"Are you sure you want to delete project {project_id}? (yes/no): ")
        if confirm.lower() == 'yes':
            del self.projects[project_id]
            self.save_data()
            print(f"\nProject {project_id} deleted successfully.")
        else:
            print("\nDeletion cancelled.")

    def generate_report(self):
        # Initialize a report
        report = Report()

        report.calc_earnings(self.invoices.values())
        report.get_late_projects(self.projects.values())
        report.get_active_work(self.projects.values())

        print("\n" + str(report))

        if report.late_projects:
            print("\nLate Projects:")
            for project in report.late_projects:
                print(f"- {project.id}: {project.title}")

        if report.active_work:
            print("\nActive Projects:")
            for project in report.active_work:
                print(f"- {project.id}: {project.title}")

        return report
    
    def export_invoice_to_txt(self):
            invoice = input("Enter invoice code to export:")
            
            if invoice not in self.invoices:
                print("Invoice Code not found.")
                return
            # Extract invoice data from dict
            invoice = self.invoices[invoice]
            
            invoice.export_to_txt()
    def add_milestone(self, project_id, name):
        if project_id not in self.projects:
            raise ValueError("Invalid Project ID.")

        project = self.projects[project_id]
        project.add_milestone(name)

        self.save_data()

    def update_milestone(self, project_id, milestone_name, new_status):
        if project_id not in self.projects:
            raise ValueError("Invalid Project ID.")

        project = self.projects[project_id]
        project.update_milestone(milestone_name, new_status)

        self.save_data()

    def show_milestone_history(self, project_id):
        if project_id not in self.projects:
            raise ValueError("Invalid Project ID.")

        project = self.projects[project_id]
        project.show_milestone_history()



def run_admin_dashboard(manager, admin_user):
    while True:
        print(f"\n--- Welcome {admin_user.name} (Admin) ---")
        print("1. View All Projects (Clients & Freelancers)")
        print("2. View All Invoices")
        print("3. Generate Full Platform Report")
        print("4. Delete Project")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            if not manager.projects:
                print("No projects in the system.")
            for p in manager.projects.values():
                print(p)
                print("-" * 30)
        elif choice == "2":
            manager.display_invoices()
        elif choice == "3":
            manager.generate_report()
        elif choice == "4":
            manager.delete_project_interactive(admin_user)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


def run_freelancer_dashboard(manager, freelancer_user):
    while True:
        print("1. View My Assigned Projects")
        print("2. Add Milestone")
        print("3. Update Milestone Status")
        print("4. View Milestone History")
        print("5. Update Project Status")
        print("6. Update Project Deadline")
        print("7. Generate Invoice")
        print("8. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            my_projects = []
            for p in manager.projects.values():
                if p.freelancer is not None:
                    if p.freelancer.id == freelancer_user.id:
                        my_projects.append(p)
            if not my_projects:
                print("You have no assigned projects.")
            else:
                for p in my_projects:
                    print(p)
                    print("-" * 30)
        elif choice == "2":
            project_id = input("Enter project ID: ")
            milestone_name = input("Enter milestone name: ")
            try:
                manager.add_milestone(project_id, milestone_name)
                print(f"\nMilestone '{milestone_name}' added successfully.")
            except ValueError as e:
                print(f"\nError: {e}")
        elif choice == "3":
            project_id = input("Enter project ID: ")
            milestone_name = input("Enter milestone name: ")
            new_status = input(
                "Enter new status (pending/in progress/completed): "
            )
            try:
                manager.update_milestone(
                    project_id,
                    milestone_name,
                    new_status
                )
                print(f"\nMilestone '{milestone_name}' updated successfully.")
            except ValueError as e:
                print(f"\nError: {e}")
        elif choice == "4":
            project_id = input("Enter project ID: ")
            try:
                manager.show_milestone_history(project_id)
            except ValueError as e:
                print(f"\nError: {e}")
        elif choice == "5":
            project_id = input("Enter project ID: ")
            new_status = input(
                "Enter new status (open/in progress/closed/cancelled): "
            )
            try:
                project = manager.update_project_status(
                    project_id,
                    new_status
                )
                print(
                    f"\nProject {project.id} status "
                    f"updated to '{project.status}'."
                )
            except ValueError as e:
                print(f"\nError: {e}")
        elif choice == "6":
            project_id = input("Enter project ID: ")
            new_deadline = input(
                "Enter new deadline (DD-MM-YYYY): "
            )
            try:
                project = manager.update_project_deadline(
                    project_id,
                    new_deadline
                )
                print(
                    f"\nProject {project.id} deadline "
                    f"updated to '{project.deadline}'."
                )
            except ValueError as e:
                print(f"\nError: {e}")
        elif choice == "7":
            manager.generate_invoice()
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please try again.")

def run_client_dashboard(manager, client_user):
    while True:
        print("1. Create Project")
        print("2. Assign Project to Freelancer")
        print("3. View My Projects Progress")
        print("4. View My Milestones")
        print("5. View My Payments & Invoices")
        print("6. Pay Invoice")
        print("7. Cancel My Project")
        print("8. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                title = input("Enter Project's Title: ")
                deadline = manager.validator.get_valid_input(
                    "Enter deadline (DD-MM-YYYY): ",
                    manager.validator.check_deadline
                )
                print("Available Budgets: 1000, 2500, 5000, 10000, 20000")
                budget = int(input("Enter budget: "))
                new_project = manager.create_project(
                    title,
                    client_user.id,
                    deadline,
                    budget
                )
                print(
                    f"\nProject created successfully! "
                    f"Project ID: {new_project.id}"
                )
            except ValueError as e:
                print(f"\nError: {e}")
        elif choice == "2":
            project_id = input("Enter project ID: ")
            freelancer_id = input("Enter freelancer ID: ")
            try:
            
                if project_id in manager.projects and manager.projects[project_id].client.id != client_user.id:
                    print("Error: You can only assign freelancers to your own projects.")
                else:
                    project = manager.assign_project(project_id, freelancer_id)
                    print(f"\nProject {project.id} assigned successfully!")
            except ValueError as e:
                print(f"\nError: {e}")        
        elif choice == "3":
            # View My Projects Progress
            my_projects = []
            for project in manager.projects.values():
                if project.client.id == client_user.id:
                    my_projects.append(project)
            if not my_projects:
                print("You have no projects.")
            else:
                for project in my_projects:
                    print(project)
                    print("-" * 30)
        elif choice == "4":
            # View My Milestones
            project_id = input("Enter project ID: ")
            if project_id not in manager.projects:
                print("Project ID not found.")
                continue
            project = manager.projects[project_id]
            if project.client.id != client_user.id:
                print("You do not have access to this project.")
                continue
            if not project.milestones:
                print("No milestones found for this project.")
            else:
                print(f"\nMilestones for Project {project.id}:")
                for milestone in project.milestones:
                    print(
                        f" {milestone['name']} : "
                        f"{milestone['status']}"
                    )
        elif choice == "5":
            try:
                client_projects = manager.get_projects_for_client(client_user.id)
                
                client_project_ids = []
                for p in client_projects:
                    client_project_ids.append(p.id)
                    
                has_invoices = False
                
                print("\n--- My Payments & Invoices ---")
                for inv in manager.invoices.values():
                    if inv.project_id in client_project_ids:
                        print(f"Invoice Code: {inv.code} | Project ID: {inv.project_id} | Amount: {inv.amount} | Commission: {inv.commission} | Status: {inv.status}")
                        has_invoices = True
                
                if not has_invoices:
                    print("No invoices found for your projects.")
                print("-" * 30)
            except Exception as e:
                print(f"Error: {e}")
        elif choice == "6":
            # Pay Invoice
            manager.mark_invoice_as_paid()
        elif choice == "7":
            project_id = input("Enter your project ID to cancel: ")
            try:
                if project_id in manager.projects and manager.projects[project_id].client.id == client_user.id:
                    project = manager.update_project_status(project_id, "cancelled")
                    print(f"\nProject {project.id} has been cancelled successfully.")
                else:
                    print("\nError: You can only cancel your own projects or Invalid Project ID.")
            except ValueError as e:
                print(f"\nError: {e}")
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please try again.")

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
            logged_in_user = None
            while True:
                try:
                    user_id = input("Enter your User ID: ")
                    password = input("Enter your password: ")
                    logged_in_user = manager.login(user_id, password)
                    print("\nLogin successful! Welcome back.")
                    print(logged_in_user.display_profile())
                    break
                except (KeyError, PermissionError) as e:
                    print(f"\nInvalid input: {e} Please enter your credentials again.\n")
                except Exception as e:
                    print(f"\nAn unexpected error occurred: {e}")
                    break
            
            if logged_in_user is not None:
                if logged_in_user.role == "Admin":
                    run_admin_dashboard(manager, logged_in_user)
                elif logged_in_user.role == "Freelancer":
                    run_freelancer_dashboard(manager, logged_in_user)
                elif logged_in_user.role == "Client":
                    run_client_dashboard(manager, logged_in_user)

        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please enter 1, 2, or 3.")