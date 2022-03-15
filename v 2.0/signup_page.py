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
from openpyxl import Workbook



def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def is_new_user(userid):
    file_exist = os.path.exists(resource_path('tweetsa_user_data.xlsx'))
    if not file_exist:
        return True
    else:
        user_data = pd.read_excel('tweetsa_user_data.xlsx')
        if user_data.empty:
            return True

        user_list = user_data['userId'].unique()

        if userid not in user_list:
            return True
        else:
            return False


def signup_page(userid):
    global user_data

    file_exist = os.path.exists(resource_path('tweetsa_user_data.xlsx'))
    if not file_exist:
        book = Workbook()
        sheet = book.active
        book.save(resource_path('tweetsa_user_data.xlsx'))
        user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')
    else:
        user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')



    new_user = tk.Tk()
    new_user.title('TweetSA')

    new_user_win = tk.ttk.Frame(new_user)
    # Set the initial theme
    style = ttkthemes.ThemedStyle(new_user)
    style.set_theme("ubuntu")

    def add_keyword(keyword, attr_type, content):
        global user_data

        user_data = user_data.append({'keyword': keyword, 'type': attr_type, 'content': content, 'userId': userid},
                                     ignore_index=True)

        user_data.to_excel('tweetsa_user_data.xlsx', index=False)

        #tkinter.messagebox.showinfo('App System Notifications', message='The information you entered has been '
                                                                        #'successfully stored in the system, '
                                                                        #'please go to the main page for '
                                                                        #'more operations.')

    def back_to_login():
        new_user.destroy()


    global img2
    global resized_img2
    global new_img2
    img2 = Image.open(resource_path('icon.png'))
    resized_img2 = img2.resize((50, 41))
    new_img2 = ImageTk.PhotoImage(resized_img2)
    title_label = tk.ttk.Label(new_user_win, text=" Tweet Search & Analysis ", compound="left", background='#1DA1F2',
                               image=new_img2, foreground="white",
                               font=("Times New Roman", 22, 'bold')).grid(row=0, column=0, rowspan=2, columnspan=8)
    blank_label = tk.ttk.Label(new_user_win).grid(row=2, column=0, rowspan=1, columnspan=8)

    first_section_label = tk.ttk.Label(new_user_win, text='1. Please fill in a concept or keyword you want to track, '
                                                          'it can either be a name \nor a symbol. '
                                                          '(e.g. BTC/bitcoin, ETH/ethereum, etc)').grid(row=3, column=0,
                                                                                                        rowspan=2,
                                                                                                        columnspan=8,
                                                                                                        sticky='w')
    keyword = tk.StringVar()
    keyword_label = tk.ttk.Label(new_user_win, text='Keyword/Concept', font=('calibre', 10, 'bold'))
    keyword_entry = tk.ttk.Entry(new_user_win, textvariable=keyword, font=('calibre', 10, 'normal'))
    keyword_label.grid(row=5, column=2, rowspan=2, columnspan=1)
    keyword_entry.grid(row=5, column=3, rowspan=2, columnspan=4, sticky='nswe')

    blank_label2 = tk.ttk.Label(new_user_win).grid(row=7, column=0, rowspan=2, columnspan=8)

    second_section_label = tk.ttk.Label(new_user_win, text='2. Please add an attribute to the concept or '
                                                           'keyword you entered above, which \ncan be a related person, '
                                                           'technology, event or co-concept.   ').grid(row=9, column=0,
                                                                                                       rowspan=2,
                                                                                                       columnspan=8,
                                                                                                       sticky='w')

    attr_type = tk.StringVar()
    attr_type_label = tk.ttk.Label(new_user_win, text='Attribute Type', font=('calibre', 10, 'bold'))
    attr_type_entry = tk.ttk.Combobox(new_user_win, textvariable=attr_type, font=('calibre', 10, 'normal'))
    attr_type_entry['values'] = ('Significant Related Persons', 'Associated Technology', 'Correlated Concept',
                                 'Influential Event')
    attr_type_label.grid(row=11, column=2, rowspan=2, columnspan=1)
    attr_type_entry.grid(row=11, column=3, rowspan=2, columnspan=4, sticky='nswe')

    attr_content = tk.StringVar()
    attr_content_label = tk.ttk.Label(new_user_win, text='Attribute Content', font=('calibre', 10, 'bold'))
    attr_content_entry = tk.ttk.Entry(new_user_win, textvariable=attr_content, font=('calibre', 10, 'normal'))
    attr_content_label.grid(row=13, column=2, rowspan=2, columnspan=1)
    attr_content_entry.grid(row=13, column=3, rowspan=2, columnspan=4, sticky='nswe')

    blank_label3 = tk.ttk.Label(new_user_win).grid(row=15, column=0, rowspan=2, columnspan=8)

    finish_btn = tk.ttk.Button(new_user_win, text='Complete Registration',
                               command=lambda: add_keyword(keyword.get(), attr_type.get(), attr_content.get()))
    finish_btn.grid(row=17, column=3, rowspan=2, columnspan=4)
    bck_btn = tk.ttk.Button(new_user_win, text='Back', command=back_to_login)
    bck_btn.grid(row=17, column=1, rowspan=2, columnspan=2)

    new_user_win.grid()
    new_user.mainloop()


#signup_page('test00')
