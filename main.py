import praw
import sqlite3
import sentiment
import chart
import tkinter as tk
from tkinter import simpledialog
from tkinter import *
import time
import threading
import prawcore.exceptions
from tkinter import messagebox

opinions = []



# Initial setup and connection to the reddit API
def redditInit(subreddit_name):
    try:
        reddit = praw.Reddit(
        client_id = "JgZGz2-DqxGbXbKWMXUVpQ", 
        client_secret = "V6FLK4hxhBIWBESrHcFuGGj6pJgzsw",  
        username = "RestNo8881",  
        password = "Intro2SE",   
        user_agent = "MyRedditBot/1.0 by RestNo8881"  
        )

        
        #Signing in to reddit with username and password 
        try:
            print("Authenticated as:", reddit.user.me()) 
        except Exception as e:
            print("Login failed:", e)

        #Get subreddit posts
        subreddit = reddit.subreddit(subreddit_name)

        topPost = subreddit.hot(limit = 2500)#Limited for optimization
        
        #create DB if one not created
        connect_db()
        clear_db()

        opinions.clear()


        for post in topPost:
            insert_db(post.id, post.title)
            print("\n")           
            
        display()
        sentimentFunc()
        return True
    except prawcore.exceptions.Redirect:
        messagebox.showerror("Subreddit Error", f"'{subreddit_name}' is not a valid subreddit. Please try again.")
        return False

# Handles connection to the database  
def connect_db():
    connect = sqlite3.connect("database.db") 
    cursor = connect.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS president(
                        id INTEGER PRIMARY KEY autoincrement, 
                        postID TEXT, 
                        post TEXT)''')

    connect.commit()
    connect.close()

# Handles clearing all rows and columns of the database after each run
def clear_db():
    connect = sqlite3.connect("database.db")
    connect.execute("DELETE FROM president") 
    connect.commit()
    connect.close()

# Handles adding data into the database
def insert_db(postID, post):
    connect = sqlite3.connect("database.db")
    connect.execute('''INSERT INTO president(postID,post) VALUES (?, ?)''', [postID, post])
    connect.commit()
    

# Checks if data was correctly added to the database
def display():
    connect = sqlite3.connect('database.db')
    cur = connect.execute('SELECT post FROM president')
    res = cur.fetchall()

    print("Number of rows in DB:", len(res))

    for i in res:
        opinions.append(i[0])

# Parses the opinions found within the entered subreddit and scored the opinions 
def sentimentFunc():
    for opinion in opinions:
        sentiment.scoreText(opinion)
        print('PERSONAL OPINIONS: \n {}'.format(opinion))


# GUI Setup
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sentiment Opinion Analyzer")

        self.state("zoomed")  
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight())) #adjusting for window/screen size

        self.subreddit_screen = SubredditEntryScreen(self)
        self.chart_screen = ChartScreen(self)

        self.subreddit_screen.pack(fill = "both", expand = True)

    # Functions used for switching between the SubredditEntryScreen and the ChartScreen
    def switch_to_chart(self, entered_name = ''):
        self.subreddit_screen.pack_forget()
        self.chart_screen.pack(fill = "both", expand = True)

        if entered_name:
            self.chart_screen.label.config(text =  entered_name.capitalize())

    def switch_to_subreddit(self):
        self.chart_screen.pack_forget()
        self.subreddit_screen.pack(fill = "both", expand = True)



#Screen1: Enter subreddit name / Go to Chart screen
class SubredditEntryScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.top_bar = tk.Frame(self, bg = "#f0f0f0")
        self.top_bar.pack(side = "top", fill = "x")

        self.chart_button = tk.Button(self.top_bar, text = "Chart", font = ("Arial", 16), command = master.switch_to_chart)
        self.chart_button.pack(side = "right", padx = 10, pady = 10)

        # Initially disable button when no chart has been generated
        self.chart_button.config(state = "disabled") 

        center = tk.Frame(self)
        center.pack(expand = True)

        label = tk.Label(center, text = "Enter the name of a subreddit (e.g. politics):", font = ("Arial", 18))
        label.pack(pady = 10)

        self.entry = tk.Entry(center, font = ("Arial", 18), width = 30)
        self.entry.pack(pady = 10)

        self.submit_btn = tk.Button(center, text = "Submit", font = ("Arial", 18), command = self.submit_subreddit)
        self.submit_btn.pack(pady = 20)

        self.animated_loading_label = tk.Label(center, text = "", font = ("Arial", 16))
        self.animated_loading_label.pack()

        self.animation_running = False

    # Handles the submit button on the main screen
    # Checks for subreddit name, activates loading animation,
    # Starts Background thread for processing chart data 
    def submit_subreddit(self):
        subreddit_name = self.entry.get().strip()
        if subreddit_name:
            self.animation_running = True
            self.animate_loading()

            # Disabling button to avoid duplicated thread and premature screen advancement
            self.submit_btn.config(state = "disabled")
            self.chart_button.config(state = "disabled")

            threading.Thread(target=self.process_and_load_chart, args = (subreddit_name,), daemon = True).start()

    # Handles animating the Loading label on the main screen
    # loops until the chart data has been processes 
    def animate_loading(self):
        def loop():
            dots = ""
            while self.animation_running:
                dots = (dots + ".") if len(dots) < 3 else ""
                self.animated_loading_label.config(text = f"Loading{dots}")
                time.sleep(0.5)
        threading.Thread(target = loop, daemon = True).start()

    # Handles stopping the program from running if the user enters an 
    # incorrect subreddit and parsing the collected chart data to chart.py to be build
    def process_and_load_chart(self, subreddit_name):
        sentiment.reset()
        hasName = redditInit(subreddit_name)

        if not hasName:
            self.after(0, lambda: self.reset_subreddit_entry_screen())
            return

        pos, neg, neu = sentiment.getPos(), sentiment.getNeg(), sentiment.getNeu()

        self.after(0, lambda: self.display_chart(pos, neg, neu, subreddit_name))

    # Resets the animated loading visual and reactivates the submit button
    def reset_subreddit_entry_screen(self):
        self.animation_running = False
        self.animated_loading_label.config(text = "")
        self.submit_btn.config(state = "normal")
        self.chart_button.config(state = "normal")

    # Handles swiching to the chart screen,
    # and displaying the initial chart (Pie Chart) 
    def display_chart(self, pos, neg, neu, subreddit_name):
        self.reset_subreddit_entry_screen()
        self.master.switch_to_chart(subreddit_name)
        self.master.chart_screen.update_data_and_show_chart(pos, neg, neu)

#Screen2: Display the chart and allow users to change chart being displayed 
class ChartScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)


        # Top bar with SubReddit button
        top_bar = tk.Frame(self, bg = "#f0f0f0")
        top_bar.pack(side="top", fill = "x")

        back_button = tk.Button(top_bar, text = "SubReddit Entry", font = ("Arial", 16), command = master.switch_to_subreddit)
        back_button.pack(side = "right", padx = 10, pady = 10)

        self.label = tk.Label(self, font=("Arial", 18))
        self.label.pack(pady=20)

        center = tk.Frame(self) 
        center.pack(side = "top", fill = "both", expand = True)  

        self.chart_container = tk.Frame(center)
        self.chart_container.pack(side = "top", anchor = "n")

        self.selected = IntVar(value = 1)
        self.button_frame = Frame(center)
        self.button_frame.pack(side="top", pady=10)

        Checkbutton(self.button_frame, text = "Pie Chart", variable = self.selected, onvalue = 1, 
                              offvalue = 0, command=self.display_chart_type).pack(side = "left", padx = 5) 
        
        Checkbutton(self.button_frame, text = "Bar Chart", variable = self.selected, onvalue = 2, 
                              offvalue = 0, command=self.display_chart_type).pack(side = "left", padx = 5) 
        
        Checkbutton(self.button_frame, text = "Spider Chart", variable = self.selected, onvalue = 3, 
                        offvalue = 0, command=self.display_chart_type).pack(side = "left", padx = 5) 

        Checkbutton(self.button_frame, text = "Polar Chart", variable = self.selected, onvalue = 4, 
                        offvalue = 0, command=self.display_chart_type).pack(side = "left", padx = 5) 

        Checkbutton(self.button_frame, text = "Doughnut Chart", variable = self.selected, onvalue = 5, 
                        offvalue = 0, command=self.display_chart_type).pack(side = "left", padx = 5) 
                

    # Assigning instance variables to the ChartScreen class 
    def update_data_and_show_chart(self, pos, neg, neu):
        self.pos, self.neg, self.neu = pos, neg, neu
        self.display_chart_type() 

    # Handles clearing the existing chart and building the user selected option
    def display_chart_type(self):
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        chart_type = self.selected.get()

        if chart_type == 1:
            chart.pieChart(self.pos, self.neg, self.neu, self.chart_container)
        elif chart_type == 2:
            chart.barChart(self.pos, self.neg, self.neu, self.chart_container)
        elif chart_type == 3:
            chart.spiderChart(self.pos, self.neg, self.neu, self.chart_container)
        elif chart_type == 4:
            chart.polarBarChart(self.pos, self.neg, self.neu, self.chart_container)
        elif chart_type == 5:
            chart.doughnutChart(self.pos, self.neg, self.neu, self.chart_container)

# Run the app 
if __name__ == "__main__":
    app = App()
    app.mainloop()
    
    

