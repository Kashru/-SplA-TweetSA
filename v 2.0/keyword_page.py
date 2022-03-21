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
from func_list import *


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


# simplified_add_page('test111', 'btc', 'Significant Persons')


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
    remove_btn.grid(row=9, column=4, rowspan=2, columnspan=3, sticky='nwse')
    bck_btn = tk.ttk.Button(kw_ppl_win, text='Back', command=kw_ppl.destroy)
    bck_btn.grid(row=9, column=2, rowspan=2, columnspan=2, sticky='nwse')
    blank_label6 = tk.ttk.Label(kw_ppl_win).grid(row=11, column=0, rowspan=2, columnspan=12)

    func_title = tk.ttk.Label(kw_ppl_win, text='---------------Functional Section: Search and Analyze---------------',
                              font=("Times New Roman", 16, 'bold')).grid(row=13, column=0, rowspan=2, columnspan=12)

    blank_label7 = tk.ttk.Label(kw_ppl_win).grid(row=15, column=0, rowspan=2, columnspan=12)

    setting_label = tk.ttk.Label(kw_ppl_win, text='▼ Basic parameter settings ▼', font=("Times New Roman", 14, 'bold')) \
        .grid(row=17, column=2, rowspan=2, columnspan=3)

    retweets_var = tk.IntVar()
    faves_var = tk.IntVar()
    max_ac_var = tk.IntVar()
    include_rt_var = tk.StringVar()
    support_var = tk.StringVar()

    date_label = tk.ttk.Label(kw_ppl_win, text='Since', font=('calibre', 10, 'bold'))
    date_entry = DateEntry(kw_ppl_win)

    date_label2 = tk.ttk.Label(kw_ppl_win, text='Until', font=('calibre', 10, 'bold'))
    date_entry2 = DateEntry(kw_ppl_win)

    retweets_label = tk.ttk.Label(kw_ppl_win, text='Min Retweets', font=('calibre', 10, 'bold'))
    retweets_entry = tk.ttk.Entry(kw_ppl_win, textvariable=retweets_var, font=('calibre', 10, 'normal'))
    retweets_var.set(100)

    faves_label = tk.ttk.Label(kw_ppl_win, text='Min Favorites', font=('calibre', 10, 'bold'))
    faves_entry = tk.ttk.Entry(kw_ppl_win, textvariable=faves_var, font=('calibre', 10, 'normal'))
    faves_var.set(100)

    max_ac_label = tk.ttk.Label(kw_ppl_win, text='Max Acquisitions', font=('calibre', 10, 'bold'))
    max_ac_entry = tk.ttk.Entry(kw_ppl_win, textvariable=max_ac_var, font=('calibre', 10, 'normal'))
    max_ac_var.set(300)

    include_label = tk.ttk.Label(kw_ppl_win, text='Include Retweets', font=('calibre', 10, 'bold'))
    include_entry = tk.ttk.Combobox(kw_ppl_win, textvariable=include_rt_var)
    include_entry['values'] = ('Yes', 'No')
    include_rt_var.set('No')

    support_label = tk.ttk.Label(kw_ppl_win, text='Auxiliary Keywords', font=('calibre', 10, 'bold'))
    support_entry = tk.ttk.Entry(kw_ppl_win, textvariable=support_var, font=('calibre', 10, 'normal'))
    support_var.set(keyword)

    date_label.grid(row=19, column=2, rowspan=2, columnspan=1, sticky='nswe')
    date_entry.grid(row=19, column=3, rowspan=2, columnspan=2, sticky='nswe')
    date_label2.grid(row=21, column=2, rowspan=2, columnspan=1, sticky='nswe')
    date_entry2.grid(row=21, column=3, rowspan=2, columnspan=2, sticky='nswe')
    retweets_label.grid(row=23, column=2, rowspan=2, columnspan=1, sticky='nswe')
    retweets_entry.grid(row=23, column=3, rowspan=2, columnspan=2, sticky='nswe')
    faves_label.grid(row=25, column=2, rowspan=2, columnspan=1, sticky='nswe')
    faves_entry.grid(row=25, column=3, rowspan=2, columnspan=2, sticky='nswe')
    max_ac_label.grid(row=27, column=2, rowspan=2, columnspan=1, sticky='nswe')
    max_ac_entry.grid(row=27, column=3, rowspan=2, columnspan=2, sticky='nswe')
    include_label.grid(row=29, column=2, rowspan=2, columnspan=1, sticky='nswe')
    include_entry.grid(row=29, column=3, rowspan=2, columnspan=2, sticky='nswe')
    support_label.grid(row=31, column=2, rowspan=2, columnspan=1, sticky='nswe')
    support_entry.grid(row=31, column=3, rowspan=2, columnspan=2, sticky='nswe')

    def kw_ppl_search():
        date = date_entry.get_date()
        date = str(date)
        date2 = date_entry2.get_date()
        date2 = str(date2)
        retweets = retweets_var.get()
        faves = faves_var.get()
        max_ac = max_ac_var.get()
        include_rt = include_rt_var.get()
        support = support_var.get()

        sppl = 'from:' + listDisp.get(tk.ACTIVE)
        print(sppl)

        if include_rt == 'No':
            sppl = sppl + ' -RT'

        sppl = support + ' ' + sppl

        df = TweetsSearch(sppl, date, date2, retweets, faves, max_ac)

        show(df)

    def kw_ppl_wordfre():
        date = date_entry.get_date()
        date = str(date)
        date2 = date_entry2.get_date()
        date2 = str(date2)
        retweets = retweets_var.get()
        faves = faves_var.get()
        max_ac = max_ac_var.get()
        include_rt = include_rt_var.get()
        support = support_var.get()

        sppl = 'from:' + listDisp.get(tk.ACTIVE)
        print(sppl)

        if include_rt == 'No':
            sppl = sppl + ' -RT'

        sppl = support + ' ' + sppl

        TweetAnalyze(support, sppl, date, date2, retweets, faves, max_ac)

    def kw_ppl_cooc():
        date = date_entry.get_date()
        date = str(date)
        date2 = date_entry2.get_date()
        date2 = str(date2)
        retweets = retweets_var.get()
        faves = faves_var.get()
        max_ac = max_ac_var.get()
        include_rt = include_rt_var.get()
        support = support_var.get()

        sppl = 'from:' + listDisp.get(tk.ACTIVE)
        print(sppl)

        if include_rt == 'No':
            sppl = sppl + ' -RT'

        sppl = support + ' ' + sppl

        df = TweetCo_occurrence(support, sppl, date, date2, retweets, faves, max_ac)

        show(df)

    search_btn = tk.ttk.Button(kw_ppl_win, text='Search', command=kw_ppl_search)
    search_btn.grid(row=19, column=7, rowspan=3, columnspan=4, sticky='nswe')

    wordfre_btn = tk.ttk.Button(kw_ppl_win, text='Analyze Word Frequency   ', command=kw_ppl_wordfre)
    wordfre_btn.grid(row=23, column=7, rowspan=3, columnspan=4, sticky='nswe')

    cooc_btn = tk.ttk.Button(kw_ppl_win, text='Analyze Co-occurrence', command=kw_ppl_cooc)
    cooc_btn.grid(row=27, column=7, rowspan=3, columnspan=4, sticky='nswe')

    blank_label8 = tk.ttk.Label(kw_ppl_win).grid(row=33, column=0, rowspan=2, columnspan=12)

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
    require_tech = require_data['content'].unique()

    listScroll = tk.ttk.Scrollbar(kw_tech_win, orient=tk.VERTICAL)
    listScroll.grid(row=5, column=10, rowspan=2, columnspan=1, sticky='nswe')
    listDisp = tk.Listbox(kw_tech_win, selectmode=tk.BROWSE, yscrollcommand=listScroll.set,
                          font=('Microsoft Light', 16))
    listDisp.grid(row=5, column=2, rowspan=2, columnspan=8, sticky='nswe')

    for tech in require_tech:
        listDisp.insert(tk.END, tech)
    listScroll.config(command=listDisp.yview)

    blank_label4 = tk.ttk.Label(kw_tech_win).grid(row=7, column=0, rowspan=2, columnspan=12)

    def add_tech():
        simplified_add_page(userid, keyword, 'Associated Technology')
        listDisp.delete(0, tk.END)
        user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')
        require_data = user_data[user_data['userId'].isin([userid])]
        require_data = require_data[require_data['keyword'].isin([keyword])]
        require_data = require_data[require_data['type'].isin(['Associated Technology'])]
        require_tech = require_data['content'].unique()

        for tech in require_tech:
            listDisp.insert(tk.END, tech)

    def remove_tech():
        user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')
        msgBox = tk.messagebox.askyesno('App System Notifications', 'Do you want to delete this item?')
        if msgBox:
            tech = listDisp.get(tk.ACTIVE)
            listDisp.delete(tk.ACTIVE)

            user_data = user_data[~(user_data['userId'].isin([userid]) &
                                    user_data['keyword'].isin([keyword]) &
                                    user_data['type'].isin(['Associated Technology']) &
                                    user_data['content'].isin([tech]))]
            user_data.to_excel('tweetsa_user_data.xlsx', index=False)

    add_btn = tk.ttk.Button(kw_tech_win, text='Add', command=add_tech)
    add_btn.grid(row=9, column=7, rowspan=2, columnspan=3, sticky='nwse')
    remove_btn = tk.ttk.Button(kw_tech_win, text='Remove', command=remove_tech)
    remove_btn.grid(row=9, column=5, rowspan=2, columnspan=2, sticky='nwse')
    bck_btn = tk.ttk.Button(kw_tech_win, text='Back', command=kw_tech.destroy)
    bck_btn.grid(row=9, column=2, rowspan=2, columnspan=2, sticky='nwse')
    blank_label6 = tk.ttk.Label(kw_tech_win).grid(row=11, column=0, rowspan=2, columnspan=12)

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
    require_cpt = require_data['content'].unique()

    listScroll = tk.ttk.Scrollbar(kw_cpt_win, orient=tk.VERTICAL)
    listScroll.grid(row=5, column=10, rowspan=2, columnspan=1, sticky='nswe')
    listDisp = tk.Listbox(kw_cpt_win, selectmode=tk.BROWSE, yscrollcommand=listScroll.set, font=('Microsoft Light', 16))
    listDisp.grid(row=5, column=2, rowspan=2, columnspan=8, sticky='nswe')

    for cpt in require_cpt:
        listDisp.insert(tk.END, cpt)
    listScroll.config(command=listDisp.yview)

    blank_label4 = tk.ttk.Label(kw_cpt_win).grid(row=7, column=0, rowspan=2, columnspan=12)

    def add_cpt():
        simplified_add_page(userid, keyword, 'Correlated Concept')
        listDisp.delete(0, tk.END)
        user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')
        require_data = user_data[user_data['userId'].isin([userid])]
        require_data = require_data[require_data['keyword'].isin([keyword])]
        require_data = require_data[require_data['type'].isin(['Correlated Concept'])]
        require_cpt = require_data['content'].unique()

        for cpt in require_cpt:
            listDisp.insert(tk.END, cpt)

    def remove_cpt():
        user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')
        msgBox = tk.messagebox.askyesno('App System Notifications', 'Do you want to delete this item?')
        if msgBox:
            tech = listDisp.get(tk.ACTIVE)
            listDisp.delete(tk.ACTIVE)

            user_data = user_data[~(user_data['userId'].isin([userid]) &
                                    user_data['keyword'].isin([keyword]) &
                                    user_data['type'].isin(['Correlated Concept']) &
                                    user_data['content'].isin([tech]))]
            user_data.to_excel('tweetsa_user_data.xlsx', index=False)

    add_btn = tk.ttk.Button(kw_cpt_win, text='Add', command=add_cpt)
    add_btn.grid(row=9, column=7, rowspan=2, columnspan=3, sticky='nwse')
    remove_btn = tk.ttk.Button(kw_cpt_win, text='Remove', command=remove_cpt)
    remove_btn.grid(row=9, column=5, rowspan=2, columnspan=2, sticky='nwse')
    bck_btn = tk.ttk.Button(kw_cpt_win, text='Back', command=kw_cpt.destroy)
    bck_btn.grid(row=9, column=2, rowspan=2, columnspan=2, sticky='nwse')
    blank_label6 = tk.ttk.Label(kw_cpt_win).grid(row=11, column=0, rowspan=2, columnspan=12)

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
    require_ev = require_data['content'].unique()

    listScroll = tk.ttk.Scrollbar(kw_ev_win, orient=tk.VERTICAL)
    listScroll.grid(row=5, column=10, rowspan=2, columnspan=1, sticky='nswe')
    listDisp = tk.Listbox(kw_ev_win, selectmode=tk.BROWSE, yscrollcommand=listScroll.set, font=('Microsoft Light', 16))
    listDisp.grid(row=5, column=2, rowspan=2, columnspan=8, sticky='nswe')

    for ev in require_ev:
        listDisp.insert(tk.END, ev)
    listScroll.config(command=listDisp.yview)

    blank_label4 = tk.ttk.Label(kw_ev_win).grid(row=7, column=0, rowspan=2, columnspan=12)

    def add_ev():
        simplified_add_page(userid, keyword, 'Influential Event')
        listDisp.delete(0, tk.END)
        user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')
        require_data = user_data[user_data['userId'].isin([userid])]
        require_data = require_data[require_data['keyword'].isin([keyword])]
        require_data = require_data[require_data['type'].isin(['Influential Event'])]
        require_ev = require_data['content'].unique()

        for ev in require_ev:
            listDisp.insert(tk.END, ev)

    def remove_ev():
        user_data = pd.read_excel(resource_path('tweetsa_user_data.xlsx'), engine='openpyxl')
        msgBox = tk.messagebox.askyesno('App System Notifications', 'Do you want to delete this item?')
        if msgBox:
            tech = listDisp.get(tk.ACTIVE)
            listDisp.delete(tk.ACTIVE)

            user_data = user_data[~(user_data['userId'].isin([userid]) &
                                    user_data['keyword'].isin([keyword]) &
                                    user_data['type'].isin(['Influential Event']) &
                                    user_data['content'].isin([tech]))]
            user_data.to_excel('tweetsa_user_data.xlsx', index=False)

    add_btn = tk.ttk.Button(kw_ev_win, text='Add', command=add_ev)
    add_btn.grid(row=9, column=7, rowspan=2, columnspan=3, sticky='nwse')
    remove_btn = tk.ttk.Button(kw_ev_win, text='Remove', command=remove_ev)
    remove_btn.grid(row=9, column=5, rowspan=2, columnspan=2, sticky='nwse')
    bck_btn = tk.ttk.Button(kw_ev_win, text='Back', command=kw_ev.destroy)
    bck_btn.grid(row=9, column=2, rowspan=2, columnspan=2, sticky='nwse')
    blank_label6 = tk.ttk.Label(kw_ev_win).grid(row=11, column=0, rowspan=2, columnspan=12)

    kw_ev_win.grid()
    kw_ev.wait_window()

# keyword_page('test111', 'btc')
