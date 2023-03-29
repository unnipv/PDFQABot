import os
import openai
openai.api_key = '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'
from collections import deque
from tkinter import *
from tkinter import filedialog
import tkinter.simpledialog as sd

class responseGenerator:
    sys_msg1 = "You are a chatbot that answers questions strictly based on information from the following sources: "
    sources = ["Manley's Technology of Biscuits, Crackers and Cookies",
               "Books by Duncan Manley",
               "Technology of Biscuits, Rusks, Crackers & Cookies with Formulations",
               "Basic Chemistry of Ingredients in Biscuits Manufacturing",
               "Handbook of bakery Industries",
               "FSSAI Handbooks",
               "FBMI - Federation of Biscuits Manual India",
               "Biscuit Baking Technology: Processing and Engineering Manual by bakerpacific",
               "Biscuit, Cookie and Cracker: Process and Recipes by Glyn Sykes, Iain Davidson",
               "Biscuit, Cookie and Cracker Production by bakerpacific",
               "The technology of wafers and waffles By Karl Tiefenbacher",
               "Baking problems solved by S. P. Cauvain and L. S. Young",
               "More baking problems solved S. P. Cauvain and L. S. Young",
               "Science and technology of enrobed and filled chocolate, confectionery and bakery products",
               "www.biscuitpeople.com",
               "www.bakerpedia.com"
               ]
    sys_msg2 = ". If the sources don't have the answer, then say that. Do not give answers from any other sources."
    context = deque(maxlen=10)

    def generateResponse(self, question):
        sys_msg = self.sys_msg1 + ','.join(self.sources) + self.sys_msg2
        messages = [{"role": "system", "content": sys_msg}]
        # messages.extend(list(self.context))
        messages.append({"role":"user", "content":question})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature= 0,
            max_tokens= 3500
        )
        response = completion.choices[0].message.content.strip('\n')
        print(sys_msg)
        self.context.append({"role":"user", "content":question})
        self.context.append({"role":"assistant", "content":response})
        return response
    
    def addSource(self, source):
        self.sources.append(source)

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

if __name__ == "__main__":

    resGen = responseGenerator()
    question = "2 vendors - Shivashakti Maida & Rohini Mills have sent their maida consignments to Uluberia factory. Despite both consignments having similar gluten percentage, moisture percentage, and within limit ash percentage, the dough consistency is varying. As the line incharge, you have isolated the issue to the quality of maida. What parameters would you check first to find root causes for dough inconsistency"

    answer = resGen.generateResponse(question)

    print(answer)