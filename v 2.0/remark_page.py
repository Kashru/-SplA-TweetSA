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


def new_remark(userid, keyword, type, content):
    user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')

    n_rm = tk.Toplevel()
    n_rm.title('TweetSA')

    n_rm_win = tk.ttk.Frame(n_rm)
    # Set the initial theme
    style = ttkthemes.ThemedStyle(n_rm)
    style.set_theme("ubuntu")

    def add_remark(remark_text):
        global user_data

        user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')

        user_data = pd.concat([user_data, pd.DataFrame({'keyword': keyword, 'type': type, 'content': content,
                                                        'userId': userid, 'remark': remark_text}, index=[0])],
                              ignore_index=True)

        user_data.to_excel('tweetsa_user_data.xlsx', index=False)

        tkinter.messagebox.showinfo('App System Notifications', message='The remark for this item has been updated.')
        n_rm.destroy()

    global img12
    global resized_img12
    global new_img12
    img12 = Image.open(resource_path('icon.png'))
    resized_img12 = img12.resize((50, 41))
    new_img12 = ImageTk.PhotoImage(resized_img12)
    blank_label_l = tk.ttk.Label(n_rm_win, text='                 ').grid(row=0, column=0, rowspan=2, columnspan=2)
    blank_label_r = tk.ttk.Label(n_rm_win, text='                 ').grid(row=0, column=10, rowspan=2, columnspan=2)
    title_label = tk.ttk.Label(n_rm_win, text=" Tweet Search & Analysis ", compound="left",
                               background='#1DA1F2',
                               image=new_img12, foreground="white",
                               font=("Times New Roman", 22, 'bold')).grid(row=0, column=2, rowspan=2, columnspan=8)
    blank_label = tk.ttk.Label(n_rm_win).grid(row=2, column=0, rowspan=1, columnspan=12)
    blank_label2 = tk.ttk.Label(n_rm_win, text='    ').grid(row=3, column=0, rowspan=2, columnspan=2)
    blank_label3 = tk.ttk.Label(n_rm_win, text='    ').grid(row=3, column=8, rowspan=2, columnspan=2)
    list_label = tk.ttk.Label(n_rm_win, text=keyword + ': ' + content,
                              font=("Times New Roman", 16, 'bold'), justify='center'). \
        grid(row=3, column=2, rowspan=2, columnspan=8)
    blank_label4 = tk.ttk.Label(n_rm_win).grid(row=5, column=0, rowspan=2, columnspan=12)
    list_label = tk.ttk.Label(n_rm_win,
                              text='▼ Please enter new remark content below ▼'). \
        grid(row=7, column=2, rowspan=2, columnspan=8)
    blank_label5 = tk.ttk.Label(n_rm_win).grid(row=9, column=0, rowspan=2, columnspan=12)
    attr_content = tk.StringVar()
    attr_content_entry = tk.ttk.Entry(n_rm_win, textvariable=attr_content, font=('calibre', 10, 'normal'))
    attr_content_entry.grid(row=11, column=2, rowspan=2, columnspan=8, sticky='nwse')
    blank_label7 = tk.ttk.Label(n_rm_win).grid(row=13, column=0, rowspan=2, columnspan=12)
    add_btn = tk.ttk.Button(n_rm_win, text='Confirm', command=lambda: add_remark(attr_content.get()))
    add_btn.grid(row=15, column=7, rowspan=2, columnspan=3, sticky='nwse')
    bck_btn = tk.ttk.Button(n_rm_win, text='Back', command=n_rm.destroy)
    bck_btn.grid(row=15, column=2, rowspan=2, columnspan=3, sticky='nwse')
    blank_label6 = tk.ttk.Label(n_rm_win).grid(row=17, column=0, rowspan=2, columnspan=12)

    n_rm_win.grid()
    n_rm.wait_window()


def delete_old_remark(userid, keyword, type, content):
    user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')
    user_data = user_data[~(user_data['userId'].isin([userid]) &
                            user_data['keyword'].isin([keyword]) &
                            user_data['type'].isin([type]) &
                            user_data['content'].isin([content]))]
    user_data.to_excel('tweetsa_user_data.xlsx', index=False)


def remark_page(userid, keyword, kw_type, content):
    user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')

    require_data = user_data[user_data['userId'].isin([userid])]
    require_data = require_data[require_data['keyword'].isin([keyword])]
    require_data = require_data[require_data['type'].isin([kw_type])]
    require_data = require_data[require_data['content'].isin([content])]
    if 'remark' not in require_data.columns:
        remark_text = 'No remark yet'

    else:
        if len(require_data['remark'].unique()) == 0:
            remark_text = 'No remark yet'
        elif pd.isna(require_data['remark'].unique()[0]):
            remark_text = 'No remark yet'
        else:
            remark_text = require_data['remark'].unique()[0]

    remark = tk.Toplevel()
    remark.title('TweetSA')

    remark_win = tk.ttk.Frame(remark)
    # Set the initial theme
    style = ttkthemes.ThemedStyle(remark)
    style.set_theme("ubuntu")

    global img11
    global resized_img11
    global new_img11
    img11 = Image.open(resource_path('icon.png'))
    resized_img11 = img11.resize((50, 41))
    new_img11 = ImageTk.PhotoImage(resized_img11)
    blank_label_l = tk.ttk.Label(remark_win, text='                 ').grid(row=0, column=0, rowspan=2, columnspan=2)
    blank_label_r = tk.ttk.Label(remark_win, text='                 ').grid(row=0, column=10, rowspan=2, columnspan=2)
    title_label = tk.ttk.Label(remark_win, text=" Tweet Search & Analysis ", compound="left",
                               background='#1DA1F2',
                               image=new_img11, foreground="white",
                               font=("Times New Roman", 22, 'bold')).grid(row=0, column=2, rowspan=2, columnspan=8)
    blank_label = tk.ttk.Label(remark_win).grid(row=2, column=0, rowspan=1, columnspan=12)
    blank_label2 = tk.ttk.Label(remark_win, text='    ').grid(row=3, column=0, rowspan=2, columnspan=2)
    blank_label3 = tk.ttk.Label(remark_win, text='    ').grid(row=3, column=8, rowspan=2, columnspan=2)
    list_label = tk.ttk.Label(remark_win, text=keyword + ': ' + content,
                              font=("Times New Roman", 18, 'bold'), justify='center'). \
        grid(row=3, column=2, rowspan=2, columnspan=8)

    blank_label4 = tk.ttk.Label(remark_win).grid(row=5, column=8, rowspan=2, columnspan=12)
    old_message = tk.Message(remark_win, text=remark_text, width=400, anchor='w', font=("Times New Roman", 16))
    old_message.grid(row=7, column=0, rowspan=2, columnspan=12)
    blank_label5 = tk.ttk.Label(remark_win).grid(row=9, column=8, rowspan=2, columnspan=12)

    def edit_remark():
        delete_old_remark(userid, keyword, kw_type, content)
        new_remark(userid, keyword, kw_type, content)
        new_user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')

        new_require_data = new_user_data[new_user_data['userId'].isin([userid])]
        new_require_data = new_require_data[new_require_data['keyword'].isin([keyword])]
        new_require_data = new_require_data[new_require_data['type'].isin([kw_type])]
        new_require_data = new_require_data[new_require_data['content'].isin([content])]
        if 'remark' not in new_require_data.columns:
            new_remark_text = 'No remark yet'

        else:
            if len(new_require_data['remark'].unique()) == 0:
                new_remark_text = 'No remark yet'
            elif pd.isna(new_require_data['remark'].unique()[0]):
                new_remark_text = 'No remark yet'
            else:
                new_remark_text = new_require_data['remark'].unique()[0]

        old_message.grid_remove()
        tk.Message(remark_win, text=new_remark_text, width=400, anchor='w',
                   font=("Times New Roman", 16)).grid(row=7, column=0, rowspan=2, columnspan=12)

    edit_btn = tk.ttk.Button(remark_win, text='Edit', command=edit_remark)
    edit_btn.grid(row=11, column=7, rowspan=2, columnspan=3, sticky='nwse')
    bck_btn = tk.ttk.Button(remark_win, text='Back', command=remark.destroy)
    bck_btn.grid(row=11, column=2, rowspan=2, columnspan=3, sticky='nwse')
    blank_label6 = tk.ttk.Label(remark_win).grid(row=13, column=0, rowspan=2, columnspan=12)

    remark_win.grid()
    remark.wait_window()

# remark_page('test111', 'eth', 'Associated Technology', 'blockchain')
