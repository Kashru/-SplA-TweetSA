import tkinter as tk

import matplotlib.pyplot as plt
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
from signup_page import *
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
        account_list = tkinter.Listbox(window_admin, fg='white', bg='black', font=('Arial', 15), bd=30, width=30)
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
            self.createPage()

        def createPage(self):
            self.page = tk.ttk.Frame(self.root)
            # Set the initial theme
            style = ttkthemes.ThemedStyle(self.root)
            style.set_theme("ubuntu")

            global img
            global resized_img
            global new_img
            img = Image.open(resource_path('icon.png'))
            resized_img = img.resize((50, 41))
            new_img = ImageTk.PhotoImage(resized_img)
            title_label = tk.ttk.Label(self.page, text=" Tweet Search & Analysis ", compound="left",
                                       background='#1DA1F2',
                                       image=new_img, foreground="white", font=("Times New Roman", 22, 'bold')).grid(
                row=0,
                column=0,
                rowspan=2,
                columnspan=8)
            blank_label = tk.ttk.Label(self.page).grid(row=2, column=0, rowspan=1, columnspan=6)
            blank_label2 = tk.ttk.Label(self.page).grid(row=7, column=0, rowspan=1, columnspan=6)
            blank_label3 = tk.ttk.Label(self.page).grid(row=15, column=0, rowspan=1, columnspan=6)

            user_label = tk.ttk.Label(self.page, text='User ID', font=('calibre', 10, 'bold'))
            user_entry = tk.ttk.Entry(self.page, textvariable=self.var_usr_name, font=('calibre', 10, 'normal'))

            psw_label = tk.ttk.Label(self.page, text='Password', font=('calibre', 10, 'bold'))
            psw_entry = tk.ttk.Entry(self.page, textvariable=self.var_usr_pwd, font=('calibre', 10, 'normal'), show='*')

            login_btn = tk.ttk.Button(self.page, text='Login', command=self.usr_login)
            signup_btn = tk.ttk.Button(self.page, text='Sign up to open an account', command=self.usr_sign_up_b)
            reset_btn = tk.ttk.Button(self.page, text='Reset password', command=self.usr_reset_pwd_b)

            user_label.grid(row=3, column=1, rowspan=2, columnspan=2, sticky='nswe')
            user_entry.grid(row=3, column=3, rowspan=2, columnspan=4, sticky='nswe')
            psw_label.grid(row=5, column=1, rowspan=2, columnspan=2, sticky='nswe')
            psw_entry.grid(row=5, column=3, rowspan=2, columnspan=4, sticky='nswe')

            login_btn.grid(row=9, column=0, rowspan=2, columnspan=8)
            signup_btn.grid(row=11, column=0, rowspan=2, columnspan=8)
            reset_btn.grid(row=13, column=0, rowspan=2, columnspan=8)

            self.page.grid()

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
                    usrs_info = {'administrator': 'integeralpha888'}
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
                        tkinter.messagebox.showinfo('App System Notifications',
                                                    message='Welcome to TweetSA, ' + usr_name + '!')
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
                        tkinter.messagebox.showerror('Warning',
                                                     'The password you entered does not match the current account, '
                                                     'please check your entry for errors and login again.')

                else:  # if cannot find the username in file
                    is_sign_up = tkinter.messagebox.askyesno('App System Notifications',
                                                             'Your account has not been registered in the local system. '
                                                             'Please sign up first.')
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
            self.root.title('TweetSA')
            self.new_name = tk.StringVar()
            self.new_pwd = tk.StringVar()
            self.new_pwd_confirm = tk.StringVar()
            self.createPage()

        def createPage(self):
            self.page = tk.ttk.Frame(self.root)
            # Set the initial theme
            style = ttkthemes.ThemedStyle(self.root)
            style.set_theme("ubuntu")
            title_label = tk.ttk.Label(self.page, text=" Tweet Search & Analysis ", compound="left",
                                       background='#1DA1F2',
                                       image=new_img, foreground="white", font=("Times New Roman", 22, 'bold')).grid(
                row=0,
                column=1,
                rowspan=2,
                columnspan=6)
            blue_label = tk.ttk.Label(self.page, text=' ', background='#1DA1F2').grid(row=0, column=0, rowspan=2,
                                                                                      columnspan=1, sticky='nswe')
            blue_label2 = tk.ttk.Label(self.page, text=' ', background='#1DA1F2').grid(row=0, column=7, rowspan=2,
                                                                                       columnspan=1, sticky='nswe')
            blank_label = tk.ttk.Label(self.page).grid(row=2, column=0, rowspan=1, columnspan=6)
            blank_label2 = tk.ttk.Label(self.page).grid(row=9, column=0, rowspan=1, columnspan=6)
            blank_label3 = tk.ttk.Label(self.page).grid(row=15, column=0, rowspan=1, columnspan=6)

            user_label = tk.ttk.Label(self.page, text='User ID', font=('calibre', 10, 'bold'))
            user_entry = tk.ttk.Entry(self.page, textvariable=self.new_name, font=('calibre', 10, 'normal'))

            psw_label = tk.ttk.Label(self.page, text='Password', font=('calibre', 10, 'bold'))
            psw_entry = tk.ttk.Entry(self.page, textvariable=self.new_pwd, font=('calibre', 10, 'normal'), show='*')

            psw_confirm_label = tk.ttk.Label(self.page, text='Confirm Password', font=('calibre', 10, 'bold'))
            psw_confirm_entry = tk.ttk.Entry(self.page, textvariable=self.new_pwd_confirm,
                                             font=('calibre', 10, 'normal'), show='*')

            signup_btn = tk.ttk.Button(self.page, text='Sign up', command=self.sign_to_python)
            back_btn = tk.ttk.Button(self.page, text='Back', command=self.Back)

            user_label.grid(row=3, column=1, rowspan=2, columnspan=2, sticky='nswe')
            user_entry.grid(row=3, column=3, rowspan=2, columnspan=4, sticky='nswe')
            psw_label.grid(row=5, column=1, rowspan=2, columnspan=2, sticky='nswe')
            psw_entry.grid(row=5, column=3, rowspan=2, columnspan=4, sticky='nswe')
            psw_confirm_label.grid(row=7, column=1, rowspan=2, columnspan=2, sticky='nswe')
            psw_confirm_entry.grid(row=7, column=3, rowspan=2, columnspan=4, sticky='nswe')

            back_btn.grid(row=11, column=0, rowspan=2, columnspan=4)
            signup_btn.grid(row=11, column=4, rowspan=2, columnspan=4)

            self.page.grid()

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
                    exist_usr_info = []
                    usrs_info = {'python': 'python'}
                    pickle.dump(usrs_info, usr_file)
                    usr_file.close()

                    # If username already exit in the file
            if nn in exist_usr_info:
                is_reset_pwd = tkinter.messagebox.showerror('Warning',
                                                            'Sorry, the username already exists, '
                                                            'please register with a different username.')
            elif np != npf:
                tkinter.messagebox.showerror('Warning',
                                             'Please make sure your passwords match!')
            else:
                if len(nn) > 15:
                    tkinter.messagebox.showerror('Warning', 'User ID must be less than 15 characters.')
                elif len(nn) < 1:
                    tkinter.messagebox.showerror('Warning', 'User ID can not be empty.')
                else:
                    if len(np) > 15:
                        tkinter.messagebox.showerror('Warning', 'Password must be less than 15 characters.')
                    elif len(np) < 3:
                        tkinter.messagebox.showerror('Warning', 'Password must be more than 3 characters')
                    else:
                        exist_usr_info[nn] = np
                        with open('usrs_info.pickle', 'wb') as usr_file:
                            pickle.dump(exist_usr_info, usr_file)
                            tkinter.messagebox.showinfo('App System Notifications',
                                                        'Your account has been successfully registered '
                                                        'to the local system. Please go back to the main page and '
                                                        'log in with your account and password.')
                            self.page.destroy()
                            LoginPage(self.root)

        def Back(self):
            self.page.destroy()
            LoginPage(self.root)

    class ResetPage(object):
        def __init__(self, master=None):
            self.root = master
            self.root.title('TweetSA')
            self.usr_name1 = tk.StringVar()
            self.old_pwd = tk.StringVar()
            self.new_pwd = tk.StringVar()
            self.new_pwd_confirm = tk.StringVar()
            self.new_pwd_confirm = tk.StringVar()
            self.createPage()

        def createPage(self):
            self.page = tk.ttk.Frame(self.root)
            # Set the initial theme
            style = ttkthemes.ThemedStyle(self.root)
            style.set_theme("ubuntu")
            title_label = tk.ttk.Label(self.page, text=" Tweet Search & Analysis ", compound="left",
                                       background='#1DA1F2',
                                       image=new_img, foreground="white", font=("Times New Roman", 22, 'bold')).grid(
                row=0,
                column=1,
                rowspan=2,
                columnspan=6)
            blue_label = tk.ttk.Label(self.page, text=' ', background='#1DA1F2').grid(row=0, column=0, rowspan=2,
                                                                                      columnspan=1, sticky='nswe')
            blue_label2 = tk.ttk.Label(self.page, text=' ', background='#1DA1F2').grid(row=0, column=7, rowspan=2,
                                                                                       columnspan=1, sticky='nswe')
            blank_label = tk.ttk.Label(self.page).grid(row=2, column=0, rowspan=1, columnspan=6)
            blank_label2 = tk.ttk.Label(self.page).grid(row=11, column=0, rowspan=1, columnspan=6)
            blank_label3 = tk.ttk.Label(self.page).grid(row=15, column=0, rowspan=1, columnspan=6)

            user_label = tk.ttk.Label(self.page, text='User ID', font=('calibre', 10, 'bold'))
            user_entry = tk.ttk.Entry(self.page, textvariable=self.usr_name1, font=('calibre', 10, 'normal'))

            psw_old_label = tk.ttk.Label(self.page, text='Original Password', font=('calibre', 10, 'bold'))
            psw_old_entry = tk.ttk.Entry(self.page, textvariable=self.old_pwd, font=('calibre', 10, 'normal'), show='*')

            psw_label = tk.ttk.Label(self.page, text='New Password', font=('calibre', 10, 'bold'))
            psw_entry = tk.ttk.Entry(self.page, textvariable=self.new_pwd, font=('calibre', 10, 'normal'), show='*')

            psw_confirm_label = tk.ttk.Label(self.page, text='Confirm Password', font=('calibre', 10, 'bold'))
            psw_confirm_entry = tk.ttk.Entry(self.page, textvariable=self.new_pwd_confirm,
                                             font=('calibre', 10, 'normal'), show='*')

            reset_btn = tk.ttk.Button(self.page, text='Reset Password', command=self.reset_pwd_python)
            back_btn = tk.ttk.Button(self.page, text='Back', command=self.Back)

            user_label.grid(row=3, column=1, rowspan=2, columnspan=2, sticky='nswe')
            user_entry.grid(row=3, column=3, rowspan=2, columnspan=4, sticky='nswe')
            psw_old_label.grid(row=5, column=1, rowspan=2, columnspan=2, sticky='nswe')
            psw_old_entry.grid(row=5, column=3, rowspan=2, columnspan=4, sticky='nswe')
            psw_label.grid(row=7, column=1, rowspan=2, columnspan=2, sticky='nswe')
            psw_entry.grid(row=7, column=3, rowspan=2, columnspan=4, sticky='nswe')
            psw_confirm_label.grid(row=9, column=1, rowspan=2, columnspan=2, sticky='nswe')
            psw_confirm_entry.grid(row=9, column=3, rowspan=2, columnspan=4, sticky='nswe')

            back_btn.grid(row=13, column=0, rowspan=2, columnspan=4)
            reset_btn.grid(row=13, column=4, rowspan=2, columnspan=4)

            self.page.grid()

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
                is_sign_up1 = tkinter.messagebox.askyesno('Warning',
                                                          'Your account has not been registered on the local system. '
                                                          'Do you want to register now?')
                if is_sign_up1:
                    self.page.destroy()
                    SignupPage(self.root)

            # If username already exit in the file
            if un in exist_usr_info:
                if op == exist_usr_info[un]:
                    if np == npc:
                        if op == np:
                            tkinter.messagebox.showerror('Warning', 'Your new password should not be the same as '
                                                                    'your current password')
                        else:
                            if len(np) > 15:
                                tkinter.messagebox.showerror('Warning', 'Password must be less than 15 characters.')
                            elif len(np) < 3:
                                tkinter.messagebox.showerror('Warning', 'Password must be more than 3 characters')
                            else:
                                exist_usr_info[un] = np
                                with open('usrs_info.pickle', 'wb') as usr_file:
                                    pickle.dump(exist_usr_info, usr_file)
                                    tkinter.messagebox.showinfo('App System Notifications',
                                                                'You have successfully reset your password.')
                                    self.page.destroy()
                                    LoginPage(self.root)
                    else:
                        tkinter.messagebox.showerror('Warning', 'Please make sure your passwords match!')
                else:
                    tkinter.messagebox.showerror('Warning', 'The password you entered for your account is incorrect. '
                                                            'Please check your entry for errors and try again.')
            else:
                is_sign_up2 = tkinter.messagebox.askyesno('Warning',
                                                          'Your account has not been registered on the local system. '
                                                          'Do you want to register now?')
                if is_sign_up2:
                    self.page.destroy()
                    SignupPage(self.root)

        def Back(self):
            self.page.destroy()
            LoginPage(self.root)

    def close_login():
        global signal
        signal += 1
        root.destroy()

    root = tk.Tk()
    LoginPage(root)
    root.protocol('WM_DELETE_WINDOW', close_login)
    root.mainloop()


global signal
signal = 1
while signal == 1:
    Login()
