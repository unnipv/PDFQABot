from tkinter import *
from tkinter import filedialog
import tkinter.simpledialog as sd
from responseGenerator import responseGenerator

resGen = responseGenerator()

def send_message():
    user_message = user_input.get()
    chat_history.config(state=NORMAL)
    chat_history.insert(END, "\nYou: " + user_message + "\n")
    bot_response = resGen.generateResponse(user_message)
    chat_history.insert(END, "\nBot: " + str(bot_response) + "\n\n")
    chat_history.config(state=DISABLED)
    user_input.delete(0, END)

def add_source():
    user_input = sd.askstring("Input", "Enter source:")
    resGen.addSource(user_input)
    chat_history.config(state=NORMAL)
    chat_history.insert(END, f"{user_input} added to sources")
    chat_history.config(state=DISABLED)

# create the root window
root = Tk()
root.title("Biscuit ChatBot")

# set the size of the window to the screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("%dx%d" % (screen_width, screen_height))

chat_history = Text(root, state=DISABLED, width = screen_width // 10, height= screen_height // 20)
chat_history.pack()

user_input = Entry(root, width=screen_width//10)
user_input.pack()
user_input.bind("<Return>", lambda x: send_message())
send_button = Button(root, text="Send", command=send_message)
send_button.pack()

source_button = Button(root, text="Add source")
source_button.pack()
source_button.config(command=add_source)

root.mainloop()