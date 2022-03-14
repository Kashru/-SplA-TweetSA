import tkinter as tk
import pandas as pd
from datetime import date
from pandas import DataFrame
import tkinter.messagebox
import pickle
from get_dash import *
from main import *

def Login():
    def destroy(x):
        x.destroy()

    def admin_check():
        with open('usrs_info.pickle', 'rb') as file:
            model = pickle.load(file)

        window_admin = tk.Tk()
        window_admin.geometry('400x400')
        window_admin.title('Administration')
        window_admin.configure(bg='black')
        account_list = tkinter.Listbox(window_admin, fg = 'white', bg='black', font=('Arial', 15), bd=30, width=30)
        account_list.pack()

        account_list.insert(tkinter.END, '| USERNAME / PASSWORD |')
        for item in model.keys():
            account_list.insert(tkinter.END, item + ' / ' + model[item])

    class LoginPage(object):
        def __init__(self, master=None):
            self.root = master
            self.root.title('Python Expenses Recorder')
            self.root.geometry('700x500')
            self.root.configure(bg='aliceblue')
            self.var_usr_name = tk.StringVar()
            self.var_usr_pwd = tk.StringVar()
            self.createPage()

        def createPage(self):
            self.page = tk.Frame(self.root)
            self.page.configure(bg='aliceblue')
            self.page.pack()
            tk.Label(self.page, text='\n\nWelcome to Python Expenses Recorder!\n', font=('Arial', 20), fg='black',
                     bg='aliceblue').pack()
            tk.Label(self.page, text='Username', font=('Arial', 15), fg='black', bg='aliceblue').pack()
            tk.Entry(self.page, textvariable=self.var_usr_name, font=('Arial', 15), fg='black', bg='white',
                     highlightbackground='whitesmoke').pack()
            tk.Label(self.page, text='Password', font=('Arial', 15), fg='black', bg='aliceblue').pack()
            tk.Entry(self.page, textvariable=self.var_usr_pwd, font=('Arial', 15), fg='black', bg='white',
                     highlightbackground='whitesmoke', show='*').pack()
            tk.Label(self.page, text='111', fg='aliceblue', bg='aliceblue').pack()
            tk.Button(self.page, text='LOGIN', command=self.usr_login, width=15, height=2, font=('Arial', 10),
                      fg='black').pack()
            tk.Label(self.page, text='111', font=('Arial', 1), fg='aliceblue', bg='aliceblue').pack()
            tk.Button(self.page, text='SIGN UP', command=self.usr_sign_up_b, width=15, height=2, font=('Arial', 10),
                      fg='black').pack()
            tk.Label(self.page, text='111', font=('Arial', 1), fg='aliceblue', bg='aliceblue').pack()
            tk.Button(self.page, text='RESET PASSWORD', command=self.usr_reset_pwd_b, width=15, height=2,
                      font=('Arial', 10),
                      fg='black').pack()

        def usr_login(self):
            usr_name = self.var_usr_name.get()
            usr_pwd = self.var_usr_pwd.get()
            global userid

            # delete the space in the tail and head of use_name
            while usr_name[-1] == ' ':
                usr_name = usr_name[:-1]
            while usr_name[0] == ' ':
                usr_name = usr_name[1:]

            try:
                with open('usrs_info.pickle', 'rb') as usr_file:
                    usrs_info = pickle.load(usr_file)
            except FileNotFoundError:

                # if cannot find the user, creat a file with a Admin 'python'
                with open('usrs_info.pickle', 'wb') as usr_file:
                    usrs_info = {'admin': '12345'}
                    pickle.dump(usrs_info, usr_file)
                    usr_file.close()

            if usr_name == 'admin':
                if usr_pwd == '12345':
                    is_check_info = tkinter.messagebox.askyesno('Administration Page',
                                                                'Hi, admin. Would you like to check all user\'s information?')
                    if is_check_info:
                        admin_check()
                else:
                    tkinter.messagebox.showerror('Error',
                                                 'Sorry, Admin. Your password is wrong, try again.')
            else:
                # See whether the username match in the file
                if usr_name in usrs_info:

                    if usr_pwd == usrs_info[usr_name]:
                        tkinter.messagebox.showinfo(message='Welcome ! ' + usr_name)
                        # userid = usr_name
                        destroy(root)
                        userid = usr_name
                        if check_new(userid):
                            new_user_page(userid)
                            dashboard(str(userid))
                        else:
                            dashboard(str(userid))

                    # if username match while password wrong
                    else:
                        tkinter.messagebox.showerror(message='Error, your password is wrong, try again.')

                else:  # if cannot find the username in file
                    is_sign_up = tkinter.messagebox.askyesno('Hi there', 'You have not sign up yet. Please sign up')
                    # ask for sign up
                    if is_sign_up:
                        self.page.destroy()
                        SignupPage(self.root)

        def usr_sign_up_b(self):
            self.page.destroy()
            SignupPage(self.root)

        def usr_reset_pwd_b(self):
            self.page.destroy()
            ResetPage(self.root)

    class SignupPage(object):
        def __init__(self, master=None):
            self.root = master
            self.root.title('Python Expenses Recorder')
            self.root.geometry('700x500')
            self.root.configure(bg='aliceblue')
            self.new_name = tk.StringVar()
            self.new_pwd = tk.StringVar()
            self.new_pwd_confirm = tk.StringVar()
            self.createPage()

        def createPage(self):
            self.page = tk.Frame(self.root)
            self.page.configure(bg='aliceblue')
            self.page.pack()
            tk.Label(self.page, text='\n\nSign Up Now\n', font=('Arial', 20), fg='black',
                     bg='aliceblue').pack()
            tk.Label(self.page, text='Username', font=('Arial', 15), fg='black', bg='aliceblue').pack()
            tk.Entry(self.page, textvariable=self.new_name, font=('Arial', 15), fg='black', bg='white',
                     highlightbackground='whitesmoke').pack()
            tk.Label(self.page, text='Password', font=('Arial', 15), fg='black', bg='aliceblue').pack()
            tk.Entry(self.page, textvariable=self.new_pwd, show='*', font=('Arial', 15), fg='black', bg='white',
                     highlightbackground='whitesmoke').pack()
            tk.Label(self.page, text='Confirm Password', font=('Arial', 15), fg='black', bg='aliceblue').pack()
            tk.Entry(self.page, textvariable=self.new_pwd_confirm, show='*', font=('Arial', 15), fg='black', bg='white',
                     highlightbackground='whitesmoke').pack()
            tk.Label(self.page, text='111', fg='aliceblue', bg='aliceblue').pack()
            tk.Button(self.page, text='SIGN UP', command=self.sign_to_python, width=15, height=2, font=('Arial', 10),
                      fg='black').pack()
            tk.Label(self.page, text='111', font=('Arial', 1), fg='aliceblue', bg='aliceblue').pack()
            tk.Button(self.page, text='BACK', command=self.Back, width=15, height=2, font=('Arial', 10),
                      fg='black').pack()

        def sign_to_python(self):
            np = self.new_pwd.get()
            npf = self.new_pwd_confirm.get()
            nn = self.new_name.get()

            # delete the space in the tail and head of nn
            while nn[-1] == ' ':
                nn = nn[:-1]
            while nn[0] == ' ':
                nn = nn[1:]

            try:
                with open('usrs_info.pickle', 'rb') as usr_file:
                    exist_usr_info = pickle.load(usr_file)
            except FileNotFoundError:
                # if cannot find the user, creat a file with a Admin 'python'
                with open('usrs_info.pickle', 'wb') as usr_file:
                    usrs_info = {'python': 'python'}
                    pickle.dump(usrs_info, usr_file)
                    usr_file.close()

                    # If username already exit in the file
            if nn in exist_usr_info:
                is_reset_pwd = tkinter.messagebox.showerror('Hi there',
                                                            'Sorry. This username have been taken, please change.')
            elif np != npf:
                tkinter.messagebox.showerror('Error',
                                             'Password and confirm password must be the same!')
            else:
                if len(nn) > 15:
                    tkinter.messagebox.showerror('Error', 'Username must be less than 15 characters!')
                elif len(nn) < 1:
                    tkinter.messagebox.showerror('Error', 'Please enter a username.')
                else:
                    if len(np) > 15:
                        tkinter.messagebox.showerror('Error', 'Password must be less than 15 characters!')
                    elif len(np) < 3:
                        tkinter.messagebox.showerror('Error', 'Password must be more than 3 characters')
                    else:
                        exist_usr_info[nn] = np
                        with open('usrs_info.pickle', 'wb') as usr_file:
                            pickle.dump(exist_usr_info, usr_file)
                            tkinter.messagebox.showinfo('Welcome', 'You have successfully signed up!')
                            self.page.destroy()
                            LoginPage(self.root)

        def Back(self):
            self.page.destroy()
            LoginPage(self.root)

    class ResetPage(object):
        def __init__(self, master=None):
            self.root = master
            self.root.title('Python Expenses Recorder')
            self.root.geometry('700x500')
            self.root.configure(bg='aliceblue')
            self.usr_name1 = tk.StringVar()
            self.old_pwd = tk.StringVar()
            self.new_pwd = tk.StringVar()
            self.new_pwd_confirm = tk.StringVar()
            self.new_pwd_confirm = tk.StringVar()
            self.createPage()

        def createPage(self):
            self.page = tk.Frame(self.root)
            self.page.configure(bg='aliceblue')
            self.page.pack()
            tk.Label(self.page, text='\n\nReset Your Password', font=('Arial', 20), fg='black',
                     bg='aliceblue').pack()
            tk.Label(self.page, text='Username', font=('Arial', 15), fg='black', bg='aliceblue').pack()
            tk.Entry(self.page, textvariable=self.usr_name1, font=('Arial', 15), fg='black', bg='white',
                     highlightbackground='whitesmoke').pack()
            tk.Label(self.page, text='Old Password', font=('Arial', 15), fg='black', bg='aliceblue').pack()
            tk.Entry(self.page, textvariable=self.old_pwd, show='*', font=('Arial', 15), fg='black', bg='white',
                     highlightbackground='whitesmoke').pack()
            tk.Label(self.page, text='New Password', font=('Arial', 15), fg='black', bg='aliceblue').pack()
            tk.Entry(self.page, textvariable=self.new_pwd, show='*', font=('Arial', 15), fg='black', bg='white',
                     highlightbackground='whitesmoke').pack()
            tk.Label(self.page, text='Confirm Password', font=('Arial', 15), fg='black', bg='aliceblue').pack()
            tk.Entry(self.page, textvariable=self.new_pwd_confirm, show='*', font=('Arial', 15), fg='black', bg='white',
                     highlightbackground='whitesmoke').pack()
            tk.Label(self.page, text='111', fg='aliceblue', bg='aliceblue').pack()
            tk.Button(self.page, text='RESET', command=self.reset_pwd_python, width=15, height=2, font=('Arial', 10),
                      fg='black').pack()
            tk.Label(self.page, text='111', font=('Arial', 1), fg='aliceblue', bg='aliceblue').pack()
            tk.Button(self.page, text='BACK', command=self.Back, width=15, height=2, font=('Arial', 10),
                      fg='black').pack()

        def reset_pwd_python(self):
            un = self.usr_name1.get()
            op = self.old_pwd.get()
            np = self.new_pwd.get()
            npc = self.new_pwd_confirm.get()

            # delete the space in the tail and head of un
            while un[-1] == ' ':
                un = un[:-1]
            while un[0] == ' ':
                un = un[1:]

            try:
                with open('usrs_info.pickle', 'rb') as usr_file:
                    exist_usr_info = pickle.load(usr_file)
            except FileNotFoundError:
                # if cannot find the user, creat a file with a Admin 'python'
                is_sign_up1 = tkinter.messagebox.askyesno('Error',
                                                          'You didn\'t sign up before, would you like to sign up?')
                if is_sign_up1:
                    self.page.destroy()
                    SignupPage(self.root)

            # If username already exit in the file
            if un in exist_usr_info:
                if op == exist_usr_info[un]:
                    if np == npc:
                        if op == np:
                            tkinter.messagebox.showerror('Error', 'New password and old password cannot be the same!')
                        else:
                            if len(np) > 15:
                                tkinter.messagebox.showerror('Error', 'Password must be less than 15 characters!')
                            elif len(np) < 3:
                                tkinter.messagebox.showerror('Error', 'Password must be more than 3 characters')
                            else:
                                exist_usr_info[un] = np
                                with open('usrs_info.pickle', 'wb') as usr_file:
                                    pickle.dump(exist_usr_info, usr_file)
                                    tkinter.messagebox.showinfo('Thank you',
                                                                'You have successfully reset the password!')
                                    self.page.destroy()
                                    LoginPage(self.root)
                    else:
                        tkinter.messagebox.showerror('Error', 'New password and confirm password must be the same!')
                else:
                    tkinter.messagebox.showerror('Error', 'The old password is wrong')
            else:
                is_sign_up2 = tkinter.messagebox.askyesno('Error',
                                                          'The username you enter did\'n sign up before, would you like to sign up?')
                if is_sign_up2:
                    self.page.destroy()
                    SignupPage(self.root)

        def Back(self):
            self.page.destroy()
            LoginPage(self.root)

    root = tk.Tk()
    LoginPage(root)
    root.mainloop()

Login()
