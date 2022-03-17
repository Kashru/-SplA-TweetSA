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
from signup_page import *


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

    def delete(listDisp):
        user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')
        msgBox = tk.messagebox.askyesno('App System Notifications', 'Are you sure you want to delete this item?')
        if msgBox:
            kw = listDisp.get(tk.ACTIVE)
            keyword = []
            keyword.append(kw)
            listDisp.delete(tk.ACTIVE)

            user_data = user_data[~user_data['keyword'].isin(keyword)]
            user_data.to_excel('tweetsa_user_data.xlsx', index=False)

    def add(listDisp, userid):
        signup_page(userid, True)
        listDisp.delete(0, tk.END)
        user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')

        keyword_list = user_data['keyword'].unique()
        for kw in keyword_list:
            listDisp.insert(tk.END, kw)


    global img3
    global resized_img3
    global new_img3
    img3 = Image.open(resource_path('icon.png'))
    resized_img3 = img3.resize((50, 41))
    new_img3 = ImageTk.PhotoImage(resized_img3)
    title_label = tk.ttk.Label(main_win, text=" Tweet Search & Analysis ", compound="left", background='#1DA1F2',
                               image=new_img3, foreground="white",
                               font=("Times New Roman", 22, 'bold')).grid(row=0, column=1, rowspan=2, columnspan=8)
    blank_label_l = tk.ttk.Label(main_win, text='           ').grid(row=0, column=0, rowspan=2, columnspan=1)
    blank_label_r = tk.ttk.Label(main_win, text='           ').grid(row=0, column=9, rowspan=2, columnspan=1)
    blank_label = tk.ttk.Label(main_win).grid(row=2, column=0, rowspan=2, columnspan=10)
    list_label = tk.ttk.Label(main_win, text='Customized Keyword/Concept List', font=("Times New Roman", 18, 'bold')).\
        grid(row=4, column=1, rowspan=2, columnspan=8)

    listScroll = tk.ttk.Scrollbar(main_win, orient=tk.VERTICAL)
    listScroll.grid(row=6, column=7, rowspan=2, columnspan=1, sticky='nswe')
    listDisp = tk.Listbox(main_win, selectmode=tk.BROWSE, yscrollcommand=listScroll.set, font=('Microsoft Light', 16))
    listDisp.grid(row=6, column=1, rowspan=2, columnspan=6, sticky='nswe')

    keyword_list = user_data['keyword'].unique()
    for kw in keyword_list:
        listDisp.insert(tk.END, kw)
    listScroll.config(command=listDisp.yview)

    blank_label4 = tk.ttk.Label(main_win).grid(row=8, column=6, rowspan=2, columnspan=8)
    logout_btn = tk.ttk.Button(main_win, text='Log out', command=logout)
    logout_btn.grid(row=10, column=1, rowspan=2, columnspan=2, sticky='nswe')

    delete_btn = tk.ttk.Button(main_win, text='Delete keyword', command=lambda: delete(listDisp))
    delete_btn.grid(row=10, column=3, rowspan=2, columnspan=1, sticky='nswe')

    add_btn = tk.ttk.Button(main_win, text='Add keyword', command=lambda: add(listDisp, userid))
    add_btn.grid(row=10, column=4, rowspan=2, columnspan=1, sticky='nswe')



    main_win.grid()
    main.mainloop()

stock_page('test111')
