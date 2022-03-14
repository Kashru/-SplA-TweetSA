import tkinter as tk
import pandas as pd
from datetime import date
from pandas import DataFrame
import tkinter.messagebox
import pickle
import tkinter as tk
from tkcalendar import DateEntry
from tkinter import messagebox
import ttkthemes
from PIL import Image, ImageTk
import webbrowser
from pandasgui import show
import sys
import os
from signup_page import*
from stock_page import *

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def Login():
    def destroy(x):
        x.destroy()

    def admin_check():
        with open('usrs_info.pickle', 'rb') as file:
            model = pickle.load(file)

        window_admin = tk.Tk()
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
            self.root.title('TweetSA')
            self.var_usr_name = tk.StringVar()
            self.var_usr_pwd = tk.StringVar()
            self.new = 1
            self.url = "https://tweetdeck.twitter.com/"
            self.createPage()

        def createPage(self):
            win = tk.ttk.Frame(self.root)
            # Set the initial theme
            style = ttkthemes.ThemedStyle(self.root)
            style.set_theme("ubuntu")

            img = Image.open(resource_path('icon.png'))
            resized_img = img.resize((50, 41))
            new_img = ImageTk.PhotoImage(resized_img)
            title_label = tk.ttk.Label(win, text=" Twitter Extraction ", compound="left", background='#1DA1F2',
                                       image=new_img, foreground="white", font=("Times New Roman", 22, 'bold')).grid(
                row=0,
                column=0,
                rowspan=2,
                columnspan=6)
            blank_label = tk.ttk.Label(win).grid(row=2, column=0, rowspan=1, columnspan=6)
            blank_label2 = tk.ttk.Label(win).grid(row=7, column=0, rowspan=1, columnspan=6)

            user_label = tk.ttk.Label(win, text='User ID', font=('calibre', 10, 'bold'))
            user_entry = tk.ttk.Entry(win, textvariable=self.var_usr_name, font=('calibre', 10, 'normal'))

            psw_label = tk.ttk.Label(win, text='Password', font=('calibre', 10, 'bold'))
            psw_entry = tk.ttk.Entry(win, textvariable=self.var_usr_pwd, font=('calibre', 10, 'normal'))

            login_btn = tk.ttk.Button(win, text='Login', command=self.usr_login)
            signup_btn = tk.ttk.Button(win, text='Sign up to open an account', command=self.usr_sign_up_b)
            reset_btn = tk.ttk.Button(win, text='Analyze Word Frequency', command=self.usr_reset_pwd_b)

            user_label.grid(row=3, column=0, rowspan=2, columnspan=2, sticky='nswe')
            user_entry.grid(row=3, column=2, rowspan=2, columnspan=4, sticky='nswe')
            psw_label.grid(row=5, column=0, rowspan=2, columnspan=2, sticky='nswe')
            psw_entry.grid(row=5, column=2, rowspan=2, columnspan=4, sticky='nswe')

            login_btn.grid(row=9, column=0, rowspan=2, columnspan=6)
            signup_btn.grid(row=11, column=0, rowspan=2, columnspan=6)
            reset_btn.grid(row=13, column=0, rowspan=2, columnspan=6)

            img2 = Image.open(resource_path('twitter.png'))
            resized_img2 = img2.resize((140, 140))
            new_img2 = ImageTk.PhotoImage(resized_img2)
            tweetdeck_btn = tk.Button(win, image=new_img2, border="0", command=self.openweb)
            tweetdeck_btn.grid(row=22, column=0, rowspan=10, columnspan=2)

            win.grid()



        def openweb(self):
            webbrowser.open(self.url, new=self.new)



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

            if usr_name == 'administrator':
                if usr_pwd == 'integeralpha888':
                    is_check_info = tkinter.messagebox.askyesno('App System Notifications',
                                                                'The administrator account is successfully logged in. '
                                                                'Would you like to check all account information in the '
                                                                'current local system?')
                    if is_check_info:
                        admin_check()
                else:
                    tkinter.messagebox.showerror('Warning',
                                                 'The password you entered does not match the current account, '
                                                 'please check your entry for errors and login again.')
            else:
                # See whether the username match in the file
                if usr_name in usrs_info:

                    if usr_pwd == usrs_info[usr_name]:
                        tkinter.messagebox.showinfo(message='Welcome ! ' + usr_name)
                        # userid = usr_name
                        destroy(root)
                        userid = usr_name
                        if is_new_user(userid):
                            signup_page(userid)
                            stock_page(str(userid))
                        else:
                            stock_page(str(userid))

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