import os
import tkinter as tk
from tkinter import Menu, filedialog, Button, Label, messagebox, ttk
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Button, Checkbutton, Entry, Frame,
# Label, LabelFrame, Menubutton, PanedWindow,
# Radiobutton, Scale, Scrollbar, and Spinbox.
# The other six are new: Combobox, Notebook, Progressbar, Separator, Sizegrip and Treeview.
# All of them are subclasses of Widget.

class Error(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self)

    def popmsg(self):
        messagebox.showinfo("information", self.msg)


class EmptydfException(Error):
    def __init__(self, msg="The Data Frame is empty!!\nLoad the .csv file first!"):
        super().__init__(msg)


class InvalidDataException(Error):
    def __init__(self, msg="The plot values are loaded with invalid data!!\nClear the data and try again!"):
        super().__init__(msg)


class myVars:
    primary_df = pd.DataFrame({})
    sorted_df = pd.DataFrame({})
    privately_owned = pd.DataFrame({})
    year = []
    count = []
    p_count = []
    lc = -1
    log = ""


def clear_data(myobj):
    myobj.primary_df = pd.DataFrame({})
    myobj.sorted_df = pd.DataFrame({})
    myobj.privately_owned = pd.DataFrame({})
    myobj.year = []
    myobj.count = []
    myobj.p_count = []
    myobj.lc += 1
    myobj.log = "\n\n[ " + str(myobj.lc) + \
        " ] : Clearing the data from the memory!"


def load_CSV(root, myobj):
    root.path = filedialog.askopenfilename(initialdir=str(os.system('cd')),
                                           title="Select a File", filetypes=(("csv files", "*.csv"), ("excel files", "*.xlsx")))
    myobj.primary_df = pd.read_csv(root.path, sep=",", encoding='Latin-1')
    myobj.lc += 1
    myobj.log = "\n\n[ " + str(myobj.lc) + \
        " ] : Loading the .csv file into the memory!"
    # primary_df.set(primary_df)


def drop_Null(myobj):
    try:
        if not myobj.primary_df.empty:
            myobj.primary_df.dropna(inplace=True, axis=1)
            myobj.lc += 1
            myobj.log = "\n\n[ " + str(myobj.lc) + \
                " ] : Dropping all missing values from the dataframe!"
        else:
            myobj.lc += 1
            myobj.log = "\n\n[ " + str(myobj.lc) + \
                " ] : EmptydfException was raised!"
            raise EmptydfException

    except EmptydfException as EDE:
        EDE.popmsg()
    # primary_df.set(primary_df)


def group_data(myobj):
    try:
        if not myobj.primary_df.empty:
            y = 1990
            myobj.sorted_df = myobj.primary_df.groupby(
                ['Incident Year']).count()

            for i in myobj.sorted_df['Record ID'].tolist():
                myobj.year.append(y)
                myobj.count.append(int(i))
                y += 1

            myobj.privately_owned = myobj.primary_df.query(
                'Operator == "PRIVATELY OWNED"')
            myobj.privately_owned = myobj.privately_owned.groupby(
                ['Incident Year']).count()

            for i in myobj.privately_owned['Record ID'].tolist():
                myobj.p_count.append(int(i))

            myobj.lc += 1
            myobj.log = "\n\n[ " + str(myobj.lc) + \
                " ] : Grouping all entries in the dataframe!"
        else:
            myobj.lc += 1
            myobj.log = "\n\n[ " + str(myobj.lc) + \
                " ] : EmptydfException was raised!"
            raise EmptydfException

    except EmptydfException as EDE:
        EDE.popmsg()


def plot_graph1(myobj, year, count):
    try:
        if len(year) == len(count) == len(range(1990, 2016)):
            myobj.lc += 1
            myobj.log = "\n\n[ " + str(myobj.lc) + \
                " ] : Plotting Graph for Year vs. No. of Incidents!\n        Fact : " + \
                str(round(np.mean(myobj.count), 0)) + \
                " aircraft incidents occurred every year."
            print_log(prg_log, myobj.log)
            y_ticks = [0, 3000, 6000, 9000, 12000, 15000]
            fig = plt.figure(figsize=(20, 4))
            plt.plot(year, count, label='No. of Incidents',
                     color='r', marker='o', markerfacecolor='k', linestyle='--', linewidth=2)
            plt.xlabel('Year')
            plt.ylabel('No. of Incidents')
            plt.legend(loc='upper left')
            plt.title('Year vs. No. of Incidents')
            plt.xticks(year)
            plt.yticks(y_ticks)
            fig.tight_layout()
            plt.grid()
            plt.show()
        else:
            myobj.lc += 1
            myobj.log = "\n\n[ " + str(myobj.lc) + \
                " ] : InvalidDataException was raised!"
            raise InvalidDataException

    except InvalidDataException as IDE:
        IDE.popmsg()


def plot_graph2(myobj, year, p_count):
    try:
        if len(year) == len(p_count) == len(range(1990, 2016)):
            myobj.lc += 1
            myobj.log = "\n\n[ " + str(myobj.lc) + \
                " ] : Plotting Graph for Year vs. No. of Incidents when the aircraft was PRIVATELY OWNED!\n        Fact : Out of the total " + \
                str(round(np.mean(myobj.count), 0)) + " aircraft events occurred every year, " + str(
                    round(np.mean(myobj.p_count), 0))+" were due to the aircrafts which were PRIVATELY OWNED."
            print_log(prg_log, myobj.log)
            y_ticks = [0, 30, 60, 90, 120, 150, 180]
            fig = plt.figure(figsize=(20, 4))
            plt.plot(year, p_count, label='No. of Incidents when the\noperator was PRIVATELY OWNED',
                     color='b', marker='o', markerfacecolor='k', linestyle='--', linewidth=2)
            plt.xlabel('Year')
            plt.ylabel(
                'No. of Incidents when the\noperator was PRIVATELY OWNED')
            plt.legend(loc='upper left')
            plt.title(
                'Year vs. No. of Incidents when the operator was PRIVATELY OWNED')
            plt.xticks(year)
            plt.yticks(y_ticks)
            fig.tight_layout()
            plt.grid()
            plt.show()
        else:
            myobj.lc += 1
            myobj.log = "\n\n[ " + str(myobj.lc) + \
                " ] : InvalidDataException was raised!"
            raise InvalidDataException

    except InvalidDataException as IDE:
        IDE.popmsg()


def printTutorial():
    tutorial = "Perform the operations in the following order :-\n\n1. Load .csv\n2. Drop missing values\n3. Group Data\n4. Show Plot\n"
    messagebox.showinfo("information", tutorial)


def printAbout():
    about = "This program is used\nto read and plot graphs\nfrom a .csv file."
    messagebox.showinfo("information", about)


def clear_logs(prg_log, myobj):
    myobj.lc = -1
    prg_log['state'] = "normal"
    prg_log.delete('1.0', 'end')
    prg_log['state'] = "disabled"


def print_log(prg_log, log):
    prg_log['state'] = "normal"
    prg_log.insert('end', log)
    prg_log['state'] = "disabled"


def construct_menubar(root, prg_log, myobj):
    menubar = Menu(root)

    menu1 = Menu(menubar, tearoff=0)
    menu1.add_command(
        label="Load .csv", command=lambda: [load_CSV(root, myobj), print_log(prg_log, myobj.log)])
    menu1.add_command(label="Drop missing values",
                      command=lambda: [drop_Null(myobj), print_log(prg_log, myobj.log)])
    menu1.add_command(label="Group Data",
                      command=lambda: [group_data(myobj), print_log(prg_log, myobj.log)])
    menu1.add_separator()
    menu1.add_command(
        label="Clear data", command=lambda: [clear_data(myobj), print_log(prg_log, myobj.log)])
    menu1.add_separator()
    menu1.add_command(label="Exit", command=lambda: [root.quit])
    menubar.add_cascade(label="Load Data", menu=menu1)

    menu2 = Menu(menubar, tearoff=0)
    menu2.add_command(label="Show Plot 1",
                      command=lambda: [plot_graph1(myobj, myobj.year, myobj.count)])
    menu2.add_command(label="Show Plot 2",
                      command=lambda: [plot_graph2(myobj, myobj.year, myobj.p_count)])
    menubar.add_cascade(label="Plot", menu=menu2)

    menu3 = Menu(menubar, tearoff=0)
    menu3.add_command(label="Tutorial", command=lambda: [printTutorial()])
    menu3.add_command(label="About", command=lambda: [printAbout()])
    menubar.add_cascade(label="Help", menu=menu3)

    root.config(menu=menubar)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Aircraft Incident Data Analysis using matplotlib and tkinter")
    myobj = myVars()
    root.geometry("500x700")
    root.pack_propagate(False)
    root.resizable(0, 0)

    prg_log = tk.Text(root, state="disabled", width=60, height=35, font=(
        "Courier New", 10), foreground="blue", wrap='none')
    prg_log.grid(padx=20, pady=50)

    ys = ttk.Scrollbar(root, orient='vertical', command=prg_log.yview)
    xs = ttk.Scrollbar(root, orient='horizontal', command=prg_log.xview)
    prg_log['yscrollcommand'] = ys.set
    prg_log['xscrollcommand'] = xs.set
    xs.grid(column=0, row=1, sticky='we')
    ys.grid(column=1, row=0, sticky='ns')

    construct_menubar(root, prg_log, myobj)

    l1 = Label(root, text="Program Log\n****************",
               font=("Times New Roman", 14))
    l1.place(relx=0.5, rely=0.037, anchor="center")

    # clr_bt_fr = tk.Frame(root).pack()
    clr_bt = Button(root, text="Clear Log", bg="purple", fg="white",
                    command=lambda: [clear_logs(prg_log, myobj)])
    clr_bt.place(relx=0.5, rely=0.92, anchor="center")

    root.mainloop()
