import tkinter as tk
import TweetSearch as tweetS
from tkcalendar import DateEntry
from tkinter import messagebox
import ttkthemes
from PIL import Image, ImageTk
import webbrowser
from pandasgui import show
import sys
import os

root = tk.Tk()
win = tk.ttk.Frame(root)

# Set the initial theme
style = ttkthemes.ThemedStyle(root)
style.set_theme("ubuntu")

root.title("Tweet Search v 1.0")

keyword_var = tk.StringVar()
justin_var = tk.StringVar()
retweets_var = tk.IntVar()
faves_var = tk.IntVar()
user_var = tk.StringVar()
verified_var = tk.StringVar()
max_ac_var = tk.IntVar()


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def search():
    keyword = keyword_var.get()
    justin = justin_var.get()
    keyword = keyword + " " + justin
    date = date_entry.get_date()
    date = str(date)
    date2 = date_entry2.get_date()
    date2 = str(date2)
    retweets = retweets_var.get()
    faves = faves_var.get()
    user = user_var.get()
    verified = verified_var.get()
    max_ac = max_ac_var.get()

    if user != '':
        keyword = keyword + " from:" + user

    if verified == 'yes':
        keyword = "filter:verified " + keyword

    df = tweetS.TweetsSearch(keyword, date, date2, retweets, faves, max_ac)
    show(df)


def userrelevant():
    keyword = keyword_var.get()
    justin = justin_var.get()
    keyword = keyword + " " + justin
    date = date_entry.get_date()
    date = str(date)
    date2 = date_entry2.get_date()
    date2 = str(date2)
    retweets = retweets_var.get()
    faves = faves_var.get()
    user = user_var.get()
    verified = verified_var.get()
    max_ac = max_ac_var.get()

    if user != '':
        keyword = keyword + " from:" + user

    if verified == 'yes':
        keyword = "filter:verified " + keyword

    tweetS.TweetUserRelevant(keyword, date, date2, retweets, faves, max_ac)


def analyze():
    keyword = keyword_var.get()
    collectionword = keyword_var.get()
    justin = justin_var.get()
    keyword = keyword + " " + justin
    date = date_entry.get_date()
    date = str(date)
    date2 = date_entry2.get_date()
    date2 = str(date2)
    retweets = retweets_var.get()
    faves = faves_var.get()
    user = user_var.get()
    verified = verified_var.get()
    max_ac = max_ac_var.get()

    if user != '':
        keyword = keyword + " from:" + user

    if verified == 'yes':
        keyword = "filter:verified " + keyword

    tweetS.TweetAnalyze(collectionword, keyword, date, date2, retweets, faves, max_ac)


def bigram():
    keyword = keyword_var.get()
    collectionword = keyword_var.get()
    justin = justin_var.get()
    keyword = keyword + " " + justin
    date = date_entry.get_date()
    date = str(date)
    date2 = date_entry2.get_date()
    date2 = str(date2)
    retweets = retweets_var.get()
    faves = faves_var.get()
    user = user_var.get()
    verified = verified_var.get()
    max_ac = max_ac_var.get()

    if user != '':
        keyword = keyword + " from:" + user

    if verified == 'yes':
        keyword = "filter:verified " + keyword

    df = tweetS.TweetCo_occurrence(collectionword, keyword, date, date2, retweets, faves, max_ac)
    show(df)


def sentiment():
    keyword = keyword_var.get()
    justin = justin_var.get()
    keyword = keyword + " " + justin
    date = date_entry.get_date()
    date = str(date)
    date2 = date_entry2.get_date()
    date2 = str(date2)
    retweets = retweets_var.get()
    faves = faves_var.get()
    user = user_var.get()
    verified = verified_var.get()
    max_ac = max_ac_var.get()

    if user != '':
        keyword = keyword + " from:" + user

    if verified == 'yes':
        keyword = "filter:verified " + keyword

    df = tweetS.TweetSentiment(keyword, date, date2, retweets, faves, max_ac)
    show(df)


def ExitApplication():
    MsgBox = tk.messagebox.askquestion('Exit Application', 'Are you sure you want to exit the application',
                                       icon='warning')
    if MsgBox == 'yes':
        root.destroy()
    else:
        tk.messagebox.showinfo('Return', 'You will now return to the application screen')


new = 1
url = "https://tweetdeck.twitter.com/"


def openweb():
    webbrowser.open(url, new=new)


keyword_label = tk.ttk.Label(win, text='Search Keyword', font=('calibre', 10, 'bold'))
keyword_entry = tk.ttk.Entry(win, textvariable=keyword_var, font=('calibre', 10, 'normal'))

user_label = tk.ttk.Label(win, text='User (if any)', font=('calibre', 10, 'bold'))
user_entry = tk.ttk.Entry(win, textvariable=user_var, font=('calibre', 10, 'normal'))

date_label = tk.ttk.Label(win, text='Since', font=('calibre', 10, 'bold'))
date_entry = DateEntry(win)

date_label2 = tk.ttk.Label(win, text='Until', font=('calibre', 10, 'bold'))
date_entry2 = DateEntry(win)

retweets_label = tk.ttk.Label(win, text='Min Retweets', font=('calibre', 10, 'bold'))
retweets_entry = tk.ttk.Entry(win, textvariable=retweets_var, font=('calibre', 10, 'normal'))
retweets_var.set(100)

faves_label = tk.ttk.Label(win, text='Min Favorites', font=('calibre', 10, 'bold'))
faves_entry = tk.ttk.Entry(win, textvariable=faves_var, font=('calibre', 10, 'normal'))
faves_var.set(100)

max_ac_label = tk.ttk.Label(win, text='Max Acquisitions', font=('calibre', 10, 'bold'))
max_ac_entry = tk.ttk.Entry(win, textvariable=max_ac_var, font=('calibre', 10, 'normal'))
max_ac_var.set(300)

img = Image.open(resource_path('icon.png'))
resized_img = img.resize((50, 41))
new_img = ImageTk.PhotoImage(resized_img)
title_label = tk.ttk.Label(win, text=" Twitter Extraction ", compound="left", background='#1DA1F2',
                           image=new_img, foreground="white", font=("Times New Roman", 22, 'bold')).grid(row=0,
                                                                                                         column=0,
                                                                                                         rowspan=2,
                                                                                                         columnspan=6)
blank_label = tk.ttk.Label(win).grid(row=2, column=0, rowspan=1, columnspan=6)
function_label = tk.ttk.Label(win, text="▼ Please select the function you need ▼",
                              font=("calibre", 12, 'bold')).grid(row=22, column=2, rowspan=2, columnspan=4)

justin_entry = tk.ttk.Combobox(win, textvariable=justin_var)
justin_entry['values'] = (' JUST IN', '')
justin_label = tk.ttk.Label(win, text='Search with', font=('calibre', 10, 'bold'))

verified_entry = tk.ttk.Combobox(win, textvariable=verified_var)
verified_entry['values'] = ('yes', 'no')
verified_label = tk.ttk.Label(win, text='Verified Accounts Only', font=('calibre', 10, 'bold'))

# creating a button using the widget
# Button that will call the submit function
search_btn = tk.ttk.Button(win, text='Search', command=search)
user_btn = tk.ttk.Button(win, text='Analyze the Most Relevant Users', command=userrelevant)
analyze_btn = tk.ttk.Button(win, text='Analyze Word Frequency', command=analyze)
bigram_btn = tk.ttk.Button(win, text='Analyze Co-occurrence and Networks of Word', command=bigram)
sentiment_btn = tk.ttk.Button(win, text='Analyze Sentiment of Tweets', command=sentiment)
quit_btn = tk.ttk.Button(win, text='Quit', command=ExitApplication)

img2 = Image.open(resource_path('twitter.png'))
resized_img2 = img2.resize((140, 140))
new_img2 = ImageTk.PhotoImage(resized_img2)
tweetdeck_btn = tk.Button(win, image=new_img2, border="0", command=openweb)

# placing the label and entry in
# the required position using grid
# method
keyword_label.grid(row=3, column=0, rowspan=2, columnspan=2, sticky='nswe')
keyword_entry.grid(row=3, column=2, rowspan=2, columnspan=4, sticky='nswe')
user_label.grid(row=5, column=0, rowspan=2, columnspan=2, sticky='nswe')
user_entry.grid(row=5, column=2, rowspan=2, columnspan=4, sticky='nswe')
justin_label.grid(row=7, column=0, rowspan=2, columnspan=2, sticky='nswe')
justin_entry.grid(row=7, column=2, rowspan=2, columnspan=4, sticky='nswe')
verified_label.grid(row=9, column=0, rowspan=2, columnspan=2, sticky='nswe')
verified_entry.grid(row=9, column=2, rowspan=2, columnspan=4, sticky='nswe')
date_label.grid(row=11, column=0, rowspan=2, columnspan=2, sticky='nswe')
date_entry.grid(row=11, column=2, rowspan=2, columnspan=4, sticky='nswe')
date_label2.grid(row=13, column=0, rowspan=2, columnspan=2, sticky='nswe')
date_entry2.grid(row=13, column=2, rowspan=2, columnspan=4, sticky='nswe')
retweets_label.grid(row=15, column=0, rowspan=2, columnspan=2, sticky='nswe')
retweets_entry.grid(row=15, column=2, rowspan=2, columnspan=4, sticky='nswe')
faves_label.grid(row=17, column=0, rowspan=2, columnspan=2, sticky='nswe')
faves_entry.grid(row=17, column=2, rowspan=2, columnspan=4, sticky='nswe')
max_ac_label.grid(row=19, column=0, rowspan=2, columnspan=2, sticky='nswe')
max_ac_entry.grid(row=19, column=2, rowspan=2, columnspan=4, sticky='nswe')

# blank_label2 = tk.ttk.Label(win).grid(row=19, column=0, rowspan=1, columnspan=6)

search_btn.grid(row=24, column=2, rowspan=2, columnspan=2, sticky='nswe')
user_btn.grid(row=26, column=2, rowspan=2, columnspan=2, sticky='nswe')
analyze_btn.grid(row=28, column=2, rowspan=2, columnspan=2, sticky='nswe')
bigram_btn.grid(row=30, column=2, rowspan=2, columnspan=2, sticky='nswe')
sentiment_btn.grid(row=32, column=2, rowspan=2, columnspan=2, sticky='nswe')

tweetdeck_btn.grid(row=22, column=0, rowspan=10, columnspan=2)
quit_btn.grid(row=32, column=0, rowspan=2, columnspan=2, sticky='ns')
# performing an infinite loop
# for the window to display

win.grid()
root.mainloop()
