import os
import openai
openai.api_key = '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'
from collections import deque

class responseGenerator:
    sys_msg1 = "You are a chatbot that answers questions strictly based on information from the following sources: "
    sys_msg2 = ". If the sources don't have the answer, then say that. Do not give answers from any other sources."
    context = deque(maxlen=10)
    sources = []

    def generateResponse(self, question):
        self.getSources()
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
        file = open("sources.txt", "a")  # append mode
        file.write("\n")
        file.write(source)
        file.close()

    def getSources(self):
        file = open("sources.txt", "r")
        data = file.read()
        file.close()
        self.sources = data.split("\n")

if __name__ == "__main__":

    resGen = responseGenerator()
    question = "2 vendors - Shivashakti Maida & Rohini Mills have sent their maida consignments to Uluberia factory. Despite both consignments having similar gluten percentage, moisture percentage, and within limit ash percentage, the dough consistency is varying. As the line incharge, you have isolated the issue to the quality of maida. What parameters would you check first to find root causes for dough inconsistency"

    answer = resGen.generateResponse(question)

    print(answer)
