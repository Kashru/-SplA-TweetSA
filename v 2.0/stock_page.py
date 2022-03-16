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
from openpyxl import Workbook


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def stock_page(userid):
    #global user_data

    file_exist = os.path.exists(resource_path('tweetsa_user_data.xlsx'))
    if not file_exist:
        book = Workbook()
        sheet = book.active
        book.save(resource_path('tweetsa_user_data.xlsx'))
        user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')
    else:
        user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')

    if 'keyword' not in user_data or userid not in user_data['userId'].unique():
        return

    main = tk.Tk()
    main.title('TweetSA')

    main_win = tk.ttk.Frame(main)
    # Set the initial theme
    style = ttkthemes.ThemedStyle(main)
    style.set_theme("ubuntu")

    def logout():
        msgBox = tk.messagebox.askquestion("App System Notifications", "Are you sure you want to log out?")
        if msgBox == 'yes':
            tk.messagebox.showinfo("App System Notifications", "See you Again!")
            main.destroy()

    global img3
    global resized_img3
    global new_img3
    img3 = Image.open(resource_path('icon.png'))
    resized_img3 = img3.resize((50, 41))
    new_img3 = ImageTk.PhotoImage(resized_img3)
    title_label = tk.ttk.Label(main_win, text=" Tweet Search & Analysis ", compound="left", background='#1DA1F2',
                               image=new_img3, foreground="white",
                               font=("Times New Roman", 22, 'bold')).grid(row=0, column=0, rowspan=2, columnspan=8)
    blank_label = tk.ttk.Label(main_win).grid(row=2, column=0, rowspan=1, columnspan=8)
    blank_label2 = tk.ttk.Label(main_win, text='    ').grid(row=3, column=0, rowspan=2, columnspan=2)
    blank_label3 = tk.ttk.Label(main_win, text='    ').grid(row=3, column=6, rowspan=2, columnspan=2)
    list_label = tk.ttk.Label(main_win, text='Customized Keyword/Concept List', font=("Times New Roman", 18, 'bold')).\
        grid(row=3, column=2, rowspan=2, columnspan=4, sticky='nswe')

    listScroll = tk.ttk.Scrollbar(main_win, orient=tk.VERTICAL)
    listScroll.grid(row=5, column=6, rowspan=2, columnspan=1, sticky='nswe')
    listDisp = tk.Listbox(main_win, selectmode=tk.BROWSE, yscrollcommand=listScroll.set, font=('Microsoft Light', 16))
    listDisp.grid(row=5, column=2, rowspan=2, columnspan=4, sticky='nswe')

    keyword_list = user_data['keyword'].unique()
    for kw in keyword_list:
        listDisp.insert(tk.END, kw)
    listScroll.config(command=listDisp.yview)

    logout_btn = tk.ttk.Button(main_win, text='Log out',command=logout)



    main_win.grid()
    main.mainloop()

#stock_page('test00')
