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


def keyword_page(userid, keyword):
    user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')

    keyword_home = tk.Toplevel()
    keyword_home.title('TweetSA')

    keyword_home_win = tk.ttk.Frame(keyword_home)
    # Set the initial theme
    style = ttkthemes.ThemedStyle(keyword_home)
    style.set_theme("ubuntu")

    global img4
    global resized_img4
    global new_img4
    img4 = Image.open(resource_path('icon.png'))
    resized_img4 = img4.resize((50, 41))
    new_img4 = ImageTk.PhotoImage(resized_img4)
    title_label = tk.ttk.Label(keyword_home_win, text=" Tweet Search & Analysis ", compound="left",
                               background='#1DA1F2',
                               image=new_img4, foreground="white",
                               font=("Times New Roman", 22, 'bold')).grid(row=0, column=0, rowspan=2, columnspan=8)
    blank_label = tk.ttk.Label(keyword_home_win).grid(row=2, column=0, rowspan=1, columnspan=8)
    blank_label2 = tk.ttk.Label(keyword_home_win, text='    ').grid(row=3, column=0, rowspan=2, columnspan=2)
    blank_label3 = tk.ttk.Label(keyword_home_win, text='    ').grid(row=3, column=6, rowspan=2, columnspan=2)
    list_label = tk.ttk.Label(keyword_home_win, text=keyword, font=("Times New Roman", 18, 'bold')). \
        grid(row=3, column=2, rowspan=2, columnspan=4, sticky='nswe')


def kw_people(userid, keyword):
    user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')

    kw_ppl = tk.Toplevel()
    kw_ppl.title('TweetSA')

    kw_ppl_win = tk.ttk.Frame(kw_ppl)
    # Set the initial theme
    style = ttkthemes.ThemedStyle(kw_ppl)
    style.set_theme("ubuntu")

    global img4
    global resized_img4
    global new_img4
    img4 = Image.open(resource_path('icon.png'))
    resized_img4 = img4.resize((50, 41))
    new_img4 = ImageTk.PhotoImage(resized_img4)
    blank_label_l = tk.ttk.Label(kw_ppl_win, text='                 ').grid(row=0, column=0, rowspan=2, columnspan=2)
    blank_label_r = tk.ttk.Label(kw_ppl_win, text='                 ').grid(row=0, column=10, rowspan=2, columnspan=2)
    title_label = tk.ttk.Label(kw_ppl_win, text=" Tweet Search & Analysis ", compound="left",
                               background='#1DA1F2',
                               image=new_img4, foreground="white",
                               font=("Times New Roman", 22, 'bold')).grid(row=0, column=2, rowspan=2, columnspan=8)
    blank_label = tk.ttk.Label(kw_ppl_win).grid(row=2, column=0, rowspan=1, columnspan=12)
    blank_label2 = tk.ttk.Label(kw_ppl_win, text='    ').grid(row=3, column=0, rowspan=2, columnspan=2)
    blank_label3 = tk.ttk.Label(kw_ppl_win, text='    ').grid(row=3, column=8, rowspan=2, columnspan=2)
    list_label = tk.ttk.Label(kw_ppl_win, text=keyword+': Significant Related Persons',
                              font=("Times New Roman", 16, 'bold'), justify='center'). \
        grid(row=3, column=2, rowspan=2, columnspan=8)

    require_data = user_data[user_data['userId'].isin([userid])]
    require_data = require_data[require_data['keyword'].isin([keyword])]
    require_data = require_data[require_data['type'].isin(['Significant Related Persons'])]
    require_ppl = require_data['content'].unique()

    listScroll = tk.ttk.Scrollbar(kw_ppl_win, orient=tk.VERTICAL)
    listScroll.grid(row=5, column=10, rowspan=2, columnspan=1, sticky='nswe')
    listDisp = tk.Listbox(kw_ppl_win, selectmode=tk.BROWSE, yscrollcommand=listScroll.set, font=('Microsoft Light', 16))
    listDisp.grid(row=5, column=2, rowspan=2, columnspan=8, sticky='nswe')

    for ppl in require_ppl:
        listDisp.insert(tk.END, ppl)
    listScroll.config(command=listDisp.yview)

    blank_label4 = tk.ttk.Label(kw_ppl_win).grid(row=7, column=6, rowspan=2, columnspan=12)

    kw_ppl_win.grid()
    kw_ppl.wait_window()

kw_people('test111', 'btc')