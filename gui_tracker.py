import webbrowser
from tkinter import Tk as tk, Frame, BOTH, Button, LEFT, TOP, BOTTOM, Label, Text, END

from pandastable import Table

import panda_db


class TestApp(Frame):

    def __init__(self, parent=None):
        self.root = tk()
        root = self.root
        self.parent = parent
        Frame.__init__(self)
        top_frame = Frame(root)
        bottom = Frame(root)
        box_frame = Frame(top_frame)
        label_frame = Frame(box_frame)
        input_frame = Frame(box_frame)
        bottom.pack(side=BOTTOM, fill=BOTH, expand=True)
        # Packings
        top_frame.pack(side=TOP)
        bottom.pack(side=BOTTOM, fill=BOTH, expand=True)
        box_frame.pack(side=LEFT)
        label_frame.pack(side=TOP)
        input_frame.pack(side=BOTTOM)

        # create the widgets for the top part of the GUI,
        # and lay them out
        self.ticker_field = Text(top_frame, width=5, height=1)
        self.time_range = Text(top_frame, width=2, height=1)
        ticker_label = Label(top_frame, text="Ticker:", width=5, height=1)
        time_label = Label(top_frame, text="Hrs", width=2, height=1)

        button1 = Button(root, text="Recent Posts", width=10, height=2, command=self.recent_posts)
        button3 = Button(root, text="Summary", width=10, height=2, command=self.trending_posts)
        button2 = Button(root, text="All Posts", width=10, height=2, command=self.all_posts)
        button4 = Button(root, text="Open Url", width=10, height=2, command=self.open_url)

        button1.pack(in_=top_frame, side=LEFT)
        button3.pack(in_=top_frame, side=LEFT)
        button2.pack(in_=top_frame, side=LEFT)
        button4.pack(in_=top_frame, side=LEFT)

        ticker_label.pack(in_=label_frame, side=LEFT)
        time_label.pack(in_=label_frame, side=LEFT)
        self.ticker_field.pack(in_=input_frame, side=LEFT)
        self.time_range.pack(in_=input_frame, side=LEFT)
        self.main = self.master
        self.main.geometry('1200x800+200+100')
        self.main.title('Table app')

        # btn2 = Button(self.root, text="Ticker Post History", command=self.button2)
        # btn2.pack()
        # urlbtn = Button(self.root, text="Open url", command=self.open_url)
        # urlbtn.pack()

        self.f = Frame(self.main)
        self.f.pack(fill=BOTH, expand=1)
        # df = panda_db.get_trending()
        df = panda_db.get_all_posts("8")
        # df = panda_db.get_posts_by_ticker("AI")

        self.table = Table(self.f, dataframe=df,
                           showtoolbar=True, showstatusbar=True)

        self.table.show()

        return

    def all_posts(self):
        date_range = str(self.time_range.get("1.0", END))
        df = panda_db.get_all_posts(date_range)
        self.table = Table(self.f, dataframe=df,
                           showtoolbar=True, showstatusbar=True)
        self.table.show()
        self.table.redraw()

    def recent_posts(self):
        ticker = str(self.ticker_field.get("1.0", END))
        print(ticker)
        date_range = str(self.time_range.get("1.0", END))
        self.f.pack_forget()
        df = panda_db.get_posts_by_ticker(ticker.upper(), date_range)
        self.f.pack(fill=BOTH, expand=1)
        self.table = Table(self.f, dataframe=df,
                           showtoolbar=True, showstatusbar=True)
        self.table.show()
        self.table.redraw()

    def trending_posts(self):
        self.f.pack_forget()
        date_range = str(self.time_range.get("1.0", END))
        df = panda_db.get_trending(date_range)
        self.f.pack(fill=BOTH, expand=1)
        self.table = Table(self.f, dataframe=df,
                           showtoolbar=True, showstatusbar=True)
        self.table.show()
        self.table.redraw()

    def open_url(self):
        url = self.table.selection_get()
        webbrowser.register('chrome',
                            None,
                            webbrowser.BackgroundBrowser(
                                "C://Users//awgra//AppData//Local//Google//Chrome//Application//chrome.exe"))
        webbrowser.get('chrome').open(url)


app = TestApp()

# launch the app
app.mainloop()

# def OnButton(self):
#     self.f.pack_forget()
#     df = panda_db.get_posts_by_ticker("TSLA")
#     self.f.pack(fill=BOTH,expand=1)
#     self.table = Table(self.f, dataframe=df,
#                        showtoolbar=True, showstatusbar=True)
#     self.table.show()
#     self.table.redraw()
#
# def OnButton3(self):
#     self.f.pack_forget()
#     df = panda_db.get_posts_by_ticker("AI")
#     self.f.pack(fill=BOTH,expand=1)
#     self.table = Table(self.f, dataframe=df,
#                        showtoolbar=True, showstatusbar=True)
#     self.table.show()
#     self.table.redraw()
