from tkinter import *
import os
import pandas as pd
import tkinter as tk
from tkinter import ttk


root = Tk(className='face_recognition_gui')
svalue = StringVar()  # defines the widget state as string

w = Entry(root, textvariable=svalue)  # adds a textarea widget
w.pack()


def train_eigen_btn_load():
    name = svalue.get()
    os.system('python face_train_eigen.py %s' % name)


def recog_eigen_btn_load():
    os.system('python face_recog_eigen.py')

def show_attendance():
    # Load the attendance.csv file as a pandas dataframe
    df = pd.read_csv('attendance.csv')

    # Create a new window to display the dataframe
    df_window = tk.Tk()
    df_window.title("Attendance")
    df_window.geometry("800x200")

    # Create a treeview to display the dataframe
    tree = ttk.Treeview(df_window)
    tree.pack(side='left')

    # Add a scrollbar to the treeview
    scrollbar = ttk.Scrollbar(df_window, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')

    tree.configure(yscrollcommand=scrollbar.set)

    # Add the columns to the treeview
    tree["columns"] = list(df.columns)

    # Format the columns
    tree.column("#0", width=0, stretch='no')
    for column in tree["columns"]:
        tree.column(column, width=275, minwidth=200)
        tree.heading(column, text=column)

    # Add the rows to the treeview
    for i in range(len(df)):
        tree.insert("", i, values=list(df.iloc[i]))

    df_window.mainloop()

trainE_btn = Button(root, text="Train (EigenFaces)", command=train_eigen_btn_load)
trainE_btn.pack()

recogE_btn = Button(root, text="Recognize (EigenFaces)", command=recog_eigen_btn_load)
recogE_btn.pack()

report = Button(root, text="Attendance Report", command=show_attendance)
report.pack()

root.mainloop()
