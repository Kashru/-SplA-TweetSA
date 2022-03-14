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
        user_list = user_data['userId'].unique()

        if userid not in user_list:
            return True
        else:
            return False

def signup_page(userid):
    user_data = pd.read_excel('tweetsa_user_data.xlsx')


