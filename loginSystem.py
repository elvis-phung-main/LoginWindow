from tkinter import *
import hashlib 


class loginService:

    # The main window is created and launched upon initialization
    def __init__(self, master):

        frame = Frame(master, height=10, width=50)
        frame.grid()

        # Title label
        label_title = Label(text = "Login Service")
        label_title.grid(row = 1,columnspan = 2)

        # Username label and text entry
        label_user = Label(text="Username")
        label_user.grid(row=2)
        self.entry_user = Entry()
        self.entry_user.grid(row=2, column=1)

        # Password label and entry
        label_password = Label(text="Password")
        label_password.grid(row=3,sticky=E)
        self.entry_password = Entry(show="●")
        self.entry_password.grid(row=3, column=1)

        # Button to login
        button_login = Button(text="Login",command=self.login)
        button_login.grid(row=5,column=0,columnspan=2)

        # Exit button
        button_exit = Button(text="Exit",fg = "red", command = frame.quit)
        button_exit.grid(row=5, column=3)

        # Register button
        button_register = Button(text="Register", command=self.register_window)
        button_register.grid(row = 5, column = 2)

        # Checkbox to stay logged in
        # self.stay_status = IntVar() # checks if the checkbox is ticked (1) or not (0)
        # stay_check = Checkbutton(master,text = "", variable=self.stay_status, activebackground="#C6C6C6")
        # stay_check.grid(row = 4,column=0, sticky=E)
        # label_check = Label(master, text = "Stay logged in")
        # label_check.grid(row = 4, column = 1, sticky=W)
        
    # The function will convert credentials to secure hashes so they cannot just be read in the text file    
    def hasher(self, credential):
        en = credential.encode("utf-8")
        return hashlib.sha224(en).hexdigest() # return the credential as a hashed product

    # Check for correct username and password combo
    def login(self):
        
        cred_list = self.write(do="result")
        # print(str(cred_list) + " " + str(len(cred_list)))

        entry_hashedUser = self.hasher(self.entry_user.get())
        entry_hashedPass = self.hasher(self.entry_password.get())

        login_status = StringVar()
        login_status.set(" ")

        w = 25 # width of widgets
        self.bottom_login_text = Label(root, textvariable=login_status, width=w)
        
        # Check through the contents of the text file
        # Lines in even indexes are usernames while passwords are in the odd indexes
        if not len(cred_list) == 0:
            for i in range(len(cred_list)):
                # Check even indexes
                if i%2 == 0:
                    # Compare your entered username to the usernames in the file
                    if entry_hashedUser == cred_list[i]:
                        # Check the next element in cred_list, which is the corresponding password
                        # and match it to the entered password
                        if entry_hashedPass == cred_list[i+1]:
                            self.logged_window(self.entry_user.get())
                            login_status.set("")
                            # Check the status of the checkbox
                            # If checked, stay logged in even after closing the window
                            # If unchecked, automatically log out upon closing
                            # if self.stay_logged():
                            #     pass
                            # else:
                            #     pass
                            login_status.set("Log in success")
                            self.bottom_login_text = Label(root, textvariable=login_status, fg="green", width=w)
                            break
                        # If the username is right but password is wrong, break
                        else: 
                            login_status.set("Log in failed")
                            self.bottom_login_text = Label(root, textvariable=login_status, fg="red", width=w)
                            break
                # If the whole list is searched and the username is still not found
                elif i == len(cred_list)-1:
                        login_status.set("Log in failed (user DNE)")
                        self.bottom_login_text = Label(root, textvariable=login_status, fg="red", width=w)    
        else:
            login_status.set("No users registered (Register now!)")
            self.bottom_login_text = Label(root, textvariable=login_status, fg="blue", width=w)
        self.bottom_login_text.grid(row=6, columnspan=2)

    # On successful login, if the checkbox is checked, the user does not have to log in next time
    def stay_logged(self):
        if self.stay_status.get() == 1: # box is checked
            return True
        else: # box is unchecked
            return False  

    # Window that shows up once you log in successfully
    def logged_window(self, user):

        accWindow = Toplevel(root)
        accWindow.resizable(False,False)
        accWindow.title("Account Window")

        # Welcome message that includes your username that you logged in with
        label_welcome = Label(accWindow, text="Welcome", font=("Helvetica", 14))
        label_welcome.grid()
        label_usernamedisplay = Label(accWindow, text = user, font=('Helvetica', 18, 'bold'), fg="brown")
        label_usernamedisplay.config(anchor=CENTER)
        label_usernamedisplay.grid(row=1,)

        # Button to log out
        button_logout = Button(accWindow, text="Log Out", fg = "red", command=accWindow.destroy)
        button_logout.grid(row=2, column=2)

    # This function writes the information to a file to store it if the credentials are good
    # The username and password must be at least 8 characters long
    # The username cannot match another existing username, the user must enter the password twice in the fields
    def register(self):
        
        # The username and password must be at least 8 characters long
        if len(self.entry_createUser.get()) >= 8 and len(self.entry_createPass.get()) >= 8:
            # Passwords do not match each other, display error message
            if self.entry_createPass.get().strip() != self.entry_remPass.get().strip():
                self.text1.set('Not matching' + " " + self.entry_createPass.get() + " " + self.entry_remPass.get())
            else:
                b = self.write(self.entry_createUser, self.entry_createPass, "read") 
                # If the username does not exist yet and is registered
                if b:
                    self.text1.set("Account is now registered")
                    self.write(self.entry_createUser, self.entry_createPass, "write")
                    # Clear fields after registeration
                    self.entry_createUser.delete(0,END)
                    self.entry_createPass.delete(0,END)
                    self.entry_remPass.delete(0,END) 

        elif not len(self.entry_user.get()) < 8:
            self.text1.set("Invalid username")
        # Cannot register without entering the same password in the both fields
        elif not len(self.entry_createPass.get()) < 8:
            self.text1.set("Invalid password")
    
    # Create a new window to allow for creating accounts with new username and password
    def register_window(self):

        rWindow = Toplevel(root)
        rWindow.resizable(False,False)
        rWindow.title("Registration")

        # Register Page Title
        self.label_reg_title = Label(rWindow, text="Register Page")
        self.label_reg_title.grid(columnspan=2)

        # Username creation label and entry
        self.label_createUser = Label(rWindow, text="Create Username")
        self.label_createUser.grid(row=1, sticky=E)
        self.entry_createUser = Entry(rWindow)
        self.entry_createUser.grid(row=1, column=1, sticky=E)

        # Password creation label and entry
        self.label_createPass = Label(rWindow, text="Create Password")
        self.label_createPass.grid(row=2, sticky=E)
        self.entry_createPass = Entry(rWindow)
        self.entry_createPass.grid(row=2, column=1, sticky=E)

        # Password Rememberance label and entry
        label_remPass = Label(rWindow, text="Re-enter Password")
        label_remPass.grid(row=3,sticky=E)
        self.entry_remPass = Entry(rWindow)
        self.entry_remPass.grid(row=3, column=1, sticky=E)
        
        # Text on the bottom appears if when user succeeds/fails in making account
        self.text1 = StringVar() # the text
        self.text1.set("Username and Password are 8+ characters\n NO LEADING OR TRAILING SPACES")
        self.bottom_text = Label(rWindow, textvariable=self.text1)
        self.bottom_text.grid(row=5, columnspan=2)

        # Create Account button
        self.button_createAccount = Button(rWindow, text="Create Account", command=self.register)
        self.button_createAccount.grid(row=4, columnspan=2)

        # Close button, closes only the register window
        button_close = Button(rWindow, text="Close", command=rWindow.destroy)
        button_close.grid(row=4, column=2, columnspan=2)

    # The write() function is for writing usernames and passwords to a file
    # if do == "read", read from file
    # if do == "write", write to the file
    # Returns True if the username is unique, False if it already exists
    # if do == "result", return a list of the lines in file
    def write(self, user=None, password=None, do=None):
        if do == "write":
            with open("creds.txt", "a+") as f:
                f.seek(0)
                hashed_user = self.hasher(user.get().strip()) 
                hashed_password = self.hasher(password.get().strip())

                f.write("\n" + hashed_user + "\n" + hashed_password)
                the_lines = f.readlines()

                # Create a list without newlines and empty lines    
                result_list = []
                for element in the_lines:
                    r_element = element.strip("\n")
                    result_list.append(r_element)
                result_list = [i for i in result_list if i != ""]

        elif do == "read":
            with open("creds.txt", "a+") as f:
                f.seek(0)
                the_lines = f.readlines()
                for line in the_lines:
                # Check if the user already exists
                # If they do, do not add them and display corresponding message
                    if self.hasher(self.entry_createUser.get().strip()) == line.strip():
                        self.text1.set("This username already exists")
                        return False # The username already exists

                # Create a list without newlines and empty lines
                result_list = []
                for element in the_lines:
                    r_element = element.strip("\n")
                    result_list.append(r_element)
                result_list = [i for i in result_list if i != ""]
                return True # The username does not exist yet, they are registered
        
        # Get the result list (no newlines)
        elif do == "result":
            with open("creds.txt", "a+") as f:
                f.seek(0)
                the_lines = f.readlines()
                # Create a list without newlines and empty lines
                self.result_list = []
                for element in the_lines:
                    r_element = element.strip("\n ")
                    self.result_list.append(r_element)
                self.result_list = [i for i in self.result_list if i != ""] # Remove empty strings
            return self.result_list    

root = Tk()
root.title("Login Window")
root.resizable(False, False)
m = loginService(root)
root.mainloop()