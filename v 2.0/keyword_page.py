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
    blank_label_l = tk.ttk.Label(keyword_home_win, text='                 ').grid(row=0, column=0, rowspan=2,
                                                                                  columnspan=2)
    blank_label_r = tk.ttk.Label(keyword_home_win, text='                 ').grid(row=0, column=10, rowspan=2,
                                                                                  columnspan=2)
    title_label = tk.ttk.Label(keyword_home_win, text=" Tweet Search & Analysis ", compound="left",
                               background='#1DA1F2',
                               image=new_img4, foreground="white",
                               font=("Times New Roman", 22, 'bold')).grid(row=0, column=2, rowspan=2, columnspan=8)
    blank_label = tk.ttk.Label(keyword_home_win).grid(row=2, column=0, rowspan=1, columnspan=12)
    blank_label2 = tk.ttk.Label(keyword_home_win, text='    ').grid(row=3, column=0, rowspan=2, columnspan=2)
    blank_label3 = tk.ttk.Label(keyword_home_win, text='    ').grid(row=3, column=8, rowspan=2, columnspan=2)
    list_label = tk.ttk.Label(keyword_home_win, text='Keyword/Concept: ' + keyword,
                              font=("Times New Roman", 16, 'bold'), justify='center'). \
        grid(row=3, column=2, rowspan=2, columnspan=8)

    blank_label4 = tk.ttk.Label(keyword_home_win).grid(row=5, column=8, rowspan=2, columnspan=12)

    ppl_btn = tk.ttk.Button(keyword_home_win, text='Significant Related Persons',
                            command=lambda: kw_people(userid, keyword))
    ppl_btn.grid(row=7, column=3, rowspan=2, columnspan=6, sticky='nswe')

    blank_label5 = tk.ttk.Label(keyword_home_win).grid(row=9, column=8, rowspan=2, columnspan=12)

    tech_btn = tk.ttk.Button(keyword_home_win, text='Associated Technology',
                             command=lambda: kw_technology(userid, keyword))
    tech_btn.grid(row=11, column=3, rowspan=2, columnspan=6, sticky='nswe')

    blank_label6 = tk.ttk.Label(keyword_home_win).grid(row=13, column=8, rowspan=2, columnspan=12)

    cpt_btn = tk.ttk.Button(keyword_home_win, text='Correlated Concept',
                            command=lambda: kw_concept(userid, keyword))
    cpt_btn.grid(row=15, column=3, rowspan=2, columnspan=6, sticky='nswe')

    blank_label7 = tk.ttk.Label(keyword_home_win).grid(row=17, column=8, rowspan=2, columnspan=12)

    ev_btn = tk.ttk.Button(keyword_home_win, text='Influential Event',
                           command=lambda: kw_event(userid, keyword))
    ev_btn.grid(row=19, column=3, rowspan=2, columnspan=6, sticky='nswe')

    blank_label7 = tk.ttk.Label(keyword_home_win).grid(row=21, column=8, rowspan=2, columnspan=12)

    keyword_home_win.grid()
    keyword_home.wait_window()


def simplified_add_page(userid, keyword, type):
    user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')

    simp_add = tk.Toplevel()
    simp_add.title('TweetSA')

    simp_add_win = tk.ttk.Frame(simp_add)
    # Set the initial theme
    style = ttkthemes.ThemedStyle(simp_add)
    style.set_theme("ubuntu")

    def add_item(content):
        global user_data

        user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')

        user_data = pd.concat([user_data, pd.DataFrame({'keyword': keyword, 'type': type, 'content': content,
                                                        'userId': userid}, index=[0])], ignore_index=True)

        user_data.to_excel('tweetsa_user_data.xlsx', index=False)

        tkinter.messagebox.showinfo('App System Notifications', message='The information you entered has been '
                                                                        'successfully added to the system.')
        simp_add.destroy()

    global img9
    global resized_img9
    global new_img9
    img9 = Image.open(resource_path('icon.png'))
    resized_img9 = img9.resize((50, 41))
    new_img9 = ImageTk.PhotoImage(resized_img9)
    blank_label_l = tk.ttk.Label(simp_add_win, text='                 ').grid(row=0, column=0, rowspan=2, columnspan=2)
    blank_label_r = tk.ttk.Label(simp_add_win, text='                 ').grid(row=0, column=10, rowspan=2, columnspan=2)
    title_label = tk.ttk.Label(simp_add_win, text=" Tweet Search & Analysis ", compound="left",
                               background='#1DA1F2',
                               image=new_img9, foreground="white",
                               font=("Times New Roman", 22, 'bold')).grid(row=0, column=2, rowspan=2, columnspan=8)
    blank_label = tk.ttk.Label(simp_add_win).grid(row=2, column=0, rowspan=1, columnspan=12)
    blank_label2 = tk.ttk.Label(simp_add_win, text='    ').grid(row=3, column=0, rowspan=2, columnspan=2)
    blank_label3 = tk.ttk.Label(simp_add_win, text='    ').grid(row=3, column=8, rowspan=2, columnspan=2)
    list_label = tk.ttk.Label(simp_add_win, text=keyword + ': ' + type,
                              font=("Times New Roman", 16, 'bold'), justify='center'). \
        grid(row=3, column=2, rowspan=2, columnspan=8)
    blank_label4 = tk.ttk.Label(simp_add_win).grid(row=5, column=0, rowspan=2, columnspan=12)
    list_label = tk.ttk.Label(simp_add_win,
                              text='▼ Please enter the ' + type + ' you want to add in the field below ▼'). \
        grid(row=7, column=2, rowspan=2, columnspan=8)
    blank_label5 = tk.ttk.Label(simp_add_win).grid(row=9, column=0, rowspan=2, columnspan=12)
    attr_content = tk.StringVar()
    attr_content_entry = tk.ttk.Entry(simp_add_win, textvariable=attr_content, font=('calibre', 10, 'normal'))
    attr_content_entry.grid(row=11, column=2, rowspan=2, columnspan=8, sticky='nwse')
    blank_label7 = tk.ttk.Label(simp_add_win).grid(row=13, column=0, rowspan=2, columnspan=12)
    add_btn = tk.ttk.Button(simp_add_win, text='Add Complete', command=lambda: add_item(attr_content.get()))
    add_btn.grid(row=15, column=7, rowspan=2, columnspan=3, sticky='nwse')
    bck_btn = tk.ttk.Button(simp_add_win, text='Back', command=simp_add.destroy)
    bck_btn.grid(row=15, column=2, rowspan=2, columnspan=3, sticky='nwse')
    blank_label6 = tk.ttk.Label(simp_add_win).grid(row=17, column=0, rowspan=2, columnspan=12)

    simp_add_win.grid()
    simp_add.wait_window()


#simplified_add_page('test111', 'btc', 'Significant Persons')


def kw_people(userid, keyword):
    user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')

    kw_ppl = tk.Toplevel()
    kw_ppl.title('TweetSA')

    kw_ppl_win = tk.ttk.Frame(kw_ppl)
    # Set the initial theme
    style = ttkthemes.ThemedStyle(kw_ppl)
    style.set_theme("ubuntu")

    global img5
    global resized_img5
    global new_img5
    img5 = Image.open(resource_path('icon.png'))
    resized_img5 = img5.resize((50, 41))
    new_img5 = ImageTk.PhotoImage(resized_img5)
    blank_label_l = tk.ttk.Label(kw_ppl_win, text='                 ').grid(row=0, column=0, rowspan=2, columnspan=2)
    blank_label_r = tk.ttk.Label(kw_ppl_win, text='                 ').grid(row=0, column=10, rowspan=2, columnspan=2)
    title_label = tk.ttk.Label(kw_ppl_win, text=" Tweet Search & Analysis ", compound="left",
                               background='#1DA1F2',
                               image=new_img5, foreground="white",
                               font=("Times New Roman", 22, 'bold')).grid(row=0, column=2, rowspan=2, columnspan=8)
    blank_label = tk.ttk.Label(kw_ppl_win).grid(row=2, column=0, rowspan=1, columnspan=12)
    blank_label2 = tk.ttk.Label(kw_ppl_win, text='    ').grid(row=3, column=0, rowspan=2, columnspan=2)
    blank_label3 = tk.ttk.Label(kw_ppl_win, text='    ').grid(row=3, column=8, rowspan=2, columnspan=2)
    list_label = tk.ttk.Label(kw_ppl_win, text=keyword + ': Significant Related Persons',
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

    blank_label4 = tk.ttk.Label(kw_ppl_win).grid(row=7, column=0, rowspan=2, columnspan=12)

    def add_ppl():
        simplified_add_page(userid, keyword, 'Significant Related Persons')
        listDisp.delete(0, tk.END)
        user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')
        require_data = user_data[user_data['userId'].isin([userid])]
        require_data = require_data[require_data['keyword'].isin([keyword])]
        require_data = require_data[require_data['type'].isin(['Significant Related Persons'])]
        require_ppl = require_data['content'].unique()

        for ppl in require_ppl:
            listDisp.insert(tk.END, ppl)

    def remove_ppl():
        user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')
        msgBox = tk.messagebox.askyesno('App System Notifications', 'Do you want to delete this item?')
        if msgBox:
            ppl = listDisp.get(tk.ACTIVE)
            listDisp.delete(tk.ACTIVE)

            user_data = user_data[~(user_data['userId'].isin([userid]) &
                                    user_data['keyword'].isin([keyword]) &
                                    user_data['type'].isin(['Significant Related Persons']) &
                                    user_data['content'].isin([ppl]))]
            user_data.to_excel('tweetsa_user_data.xlsx', index=False)

    add_btn = tk.ttk.Button(kw_ppl_win, text='Add', command=add_ppl)
    add_btn.grid(row=9, column=7, rowspan=2, columnspan=3, sticky='nwse')
    remove_btn = tk.ttk.Button(kw_ppl_win, text='Remove', command=remove_ppl)
    remove_btn.grid(row=9, column=5, rowspan=2, columnspan=2, sticky='nwse')
    bck_btn = tk.ttk.Button(kw_ppl_win, text='Back', command=kw_ppl.destroy)
    bck_btn.grid(row=9, column=2, rowspan=2, columnspan=2, sticky='nwse')
    blank_label6 = tk.ttk.Label(kw_ppl_win).grid(row=11, column=0, rowspan=2, columnspan=12)

    kw_ppl_win.grid()
    kw_ppl.wait_window()


kw_people('test111', 'eth')


def kw_technology(userid, keyword):
    user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')

    kw_tech = tk.Toplevel()
    kw_tech.title('TweetSA')

    kw_tech_win = tk.ttk.Frame(kw_tech)
    # Set the initial theme
    style = ttkthemes.ThemedStyle(kw_tech)
    style.set_theme("ubuntu")

    global img6
    global resized_img6
    global new_img6
    img6 = Image.open(resource_path('icon.png'))
    resized_img6 = img6.resize((50, 41))
    new_img6 = ImageTk.PhotoImage(resized_img6)
    blank_label_l = tk.ttk.Label(kw_tech_win, text='                 ').grid(row=0, column=0, rowspan=2, columnspan=2)
    blank_label_r = tk.ttk.Label(kw_tech_win, text='                 ').grid(row=0, column=10, rowspan=2, columnspan=2)
    title_label = tk.ttk.Label(kw_tech_win, text=" Tweet Search & Analysis ", compound="left",
                               background='#1DA1F2',
                               image=new_img6, foreground="white",
                               font=("Times New Roman", 22, 'bold')).grid(row=0, column=2, rowspan=2, columnspan=8)
    blank_label = tk.ttk.Label(kw_tech_win).grid(row=2, column=0, rowspan=1, columnspan=12)
    blank_label2 = tk.ttk.Label(kw_tech_win, text='    ').grid(row=3, column=0, rowspan=2, columnspan=2)
    blank_label3 = tk.ttk.Label(kw_tech_win, text='    ').grid(row=3, column=8, rowspan=2, columnspan=2)
    list_label = tk.ttk.Label(kw_tech_win, text=keyword + ': Associated Technology',
                              font=("Times New Roman", 16, 'bold'), justify='center'). \
        grid(row=3, column=2, rowspan=2, columnspan=8)

    require_data = user_data[user_data['userId'].isin([userid])]
    require_data = require_data[require_data['keyword'].isin([keyword])]
    require_data = require_data[require_data['type'].isin(['Associated Technology'])]
    require_ppl = require_data['content'].unique()

    listScroll = tk.ttk.Scrollbar(kw_tech_win, orient=tk.VERTICAL)
    listScroll.grid(row=5, column=10, rowspan=2, columnspan=1, sticky='nswe')
    listDisp = tk.Listbox(kw_tech_win, selectmode=tk.BROWSE, yscrollcommand=listScroll.set,
                          font=('Microsoft Light', 16))
    listDisp.grid(row=5, column=2, rowspan=2, columnspan=8, sticky='nswe')

    for ppl in require_ppl:
        listDisp.insert(tk.END, ppl)
    listScroll.config(command=listDisp.yview)

    blank_label4 = tk.ttk.Label(kw_tech_win).grid(row=7, column=0, rowspan=2, columnspan=12)

    kw_tech_win.grid()
    kw_tech.wait_window()


def kw_concept(userid, keyword):
    user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')

    kw_cpt = tk.Toplevel()
    kw_cpt.title('TweetSA')

    kw_cpt_win = tk.ttk.Frame(kw_cpt)
    # Set the initial theme
    style = ttkthemes.ThemedStyle(kw_cpt)
    style.set_theme("ubuntu")

    global img7
    global resized_img7
    global new_img7
    img7 = Image.open(resource_path('icon.png'))
    resized_img7 = img7.resize((50, 41))
    new_img7 = ImageTk.PhotoImage(resized_img7)
    blank_label_l = tk.ttk.Label(kw_cpt_win, text='                 ').grid(row=0, column=0, rowspan=2, columnspan=2)
    blank_label_r = tk.ttk.Label(kw_cpt_win, text='                 ').grid(row=0, column=10, rowspan=2, columnspan=2)
    title_label = tk.ttk.Label(kw_cpt_win, text=" Tweet Search & Analysis ", compound="left",
                               background='#1DA1F2',
                               image=new_img7, foreground="white",
                               font=("Times New Roman", 22, 'bold')).grid(row=0, column=2, rowspan=2, columnspan=8)
    blank_label = tk.ttk.Label(kw_cpt_win).grid(row=2, column=0, rowspan=1, columnspan=12)
    blank_label2 = tk.ttk.Label(kw_cpt_win, text='    ').grid(row=3, column=0, rowspan=2, columnspan=2)
    blank_label3 = tk.ttk.Label(kw_cpt_win, text='    ').grid(row=3, column=8, rowspan=2, columnspan=2)
    list_label = tk.ttk.Label(kw_cpt_win, text=keyword + ': Correlated Concept',
                              font=("Times New Roman", 16, 'bold'), justify='center'). \
        grid(row=3, column=2, rowspan=2, columnspan=8)

    require_data = user_data[user_data['userId'].isin([userid])]
    require_data = require_data[require_data['keyword'].isin([keyword])]
    require_data = require_data[require_data['type'].isin(['Correlated Concept'])]
    require_ppl = require_data['content'].unique()

    listScroll = tk.ttk.Scrollbar(kw_cpt_win, orient=tk.VERTICAL)
    listScroll.grid(row=5, column=10, rowspan=2, columnspan=1, sticky='nswe')
    listDisp = tk.Listbox(kw_cpt_win, selectmode=tk.BROWSE, yscrollcommand=listScroll.set, font=('Microsoft Light', 16))
    listDisp.grid(row=5, column=2, rowspan=2, columnspan=8, sticky='nswe')

    for ppl in require_ppl:
        listDisp.insert(tk.END, ppl)
    listScroll.config(command=listDisp.yview)

    blank_label4 = tk.ttk.Label(kw_cpt_win).grid(row=7, column=0, rowspan=2, columnspan=12)

    kw_cpt_win.grid()
    kw_cpt.wait_window()


def kw_event(userid, keyword):
    user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')

    kw_ev = tk.Toplevel()
    kw_ev.title('TweetSA')

    kw_ev_win = tk.ttk.Frame(kw_ev)
    # Set the initial theme
    style = ttkthemes.ThemedStyle(kw_ev)
    style.set_theme("ubuntu")

    global img8
    global resized_img8
    global new_img8
    img8 = Image.open(resource_path('icon.png'))
    resized_img8 = img8.resize((50, 41))
    new_img8 = ImageTk.PhotoImage(resized_img8)
    blank_label_l = tk.ttk.Label(kw_ev_win, text='                 ').grid(row=0, column=0, rowspan=2, columnspan=2)
    blank_label_r = tk.ttk.Label(kw_ev_win, text='                 ').grid(row=0, column=10, rowspan=2, columnspan=2)
    title_label = tk.ttk.Label(kw_ev_win, text=" Tweet Search & Analysis ", compound="left",
                               background='#1DA1F2',
                               image=new_img8, foreground="white",
                               font=("Times New Roman", 22, 'bold')).grid(row=0, column=2, rowspan=2, columnspan=8)
    blank_label = tk.ttk.Label(kw_ev_win).grid(row=2, column=0, rowspan=1, columnspan=12)
    blank_label2 = tk.ttk.Label(kw_ev_win, text='    ').grid(row=3, column=0, rowspan=2, columnspan=2)
    blank_label3 = tk.ttk.Label(kw_ev_win, text='    ').grid(row=3, column=8, rowspan=2, columnspan=2)
    list_label = tk.ttk.Label(kw_ev_win, text=keyword + ': Influential Event',
                              font=("Times New Roman", 16, 'bold'), justify='center'). \
        grid(row=3, column=2, rowspan=2, columnspan=8)

    require_data = user_data[user_data['userId'].isin([userid])]
    require_data = require_data[require_data['keyword'].isin([keyword])]
    require_data = require_data[require_data['type'].isin(['Influential Event'])]
    require_ppl = require_data['content'].unique()

    listScroll = tk.ttk.Scrollbar(kw_ev_win, orient=tk.VERTICAL)
    listScroll.grid(row=5, column=10, rowspan=2, columnspan=1, sticky='nswe')
    listDisp = tk.Listbox(kw_ev_win, selectmode=tk.BROWSE, yscrollcommand=listScroll.set, font=('Microsoft Light', 16))
    listDisp.grid(row=5, column=2, rowspan=2, columnspan=8, sticky='nswe')

    for ppl in require_ppl:
        listDisp.insert(tk.END, ppl)
    listScroll.config(command=listDisp.yview)

    blank_label4 = tk.ttk.Label(kw_ev_win).grid(row=7, column=0, rowspan=2, columnspan=12)

    kw_ev_win.grid()
    kw_ev.wait_window()

# keyword_page('test111', 'btc')
