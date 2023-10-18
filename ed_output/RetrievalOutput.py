""" This class works with the robbert model class.
To provide a response given a detected emotion.
The response comes from the database"""
import random as rd
from typing import List


class RetrievalOutput:
    def __init__(self, conn, cur, epsilon, ed_model):
        self.database = conn,
        self.cur = cur
        self.memory = []
        self.ed_model = ed_model
        self.conv_id = 0
        self.epsilon = epsilon
        self. categories = {"pos": ["joy", "love"], "neu": ["neutral", "other"], "neg": ["sad", "angry", "fear"]}
        self.grading = {"neg-neg": -1, "neg-neu": 1, "neg-pos": 2, "neu-neu": 0, "neu-pos": 1, "neu-neg": -1, "pos-pos": 1, "pos-neu": 0, "pos-neg": -2}

    def check_emotion(self, text: str) -> str:
        # in this function get the emotion of a text
        emotion = self.ed_model.predict(text)
        # small print statement to show in the test conversation
        print("detected_emotion:", emotion.strip(" "))
        return emotion

    def get_output(self, emotion:str):
        # retrieve from db using policy greedy
        if emotion != "neutral" and emotion != "other":
          rd_int = round(rd.random(), 2)
          if rd_int > self.epsilon:
            # random
            query = "SELECT id, output, emotion, score FROM outputs WHERE emotion = '%s' ORDER BY RANDOM() LIMIT 1" % emotion
          else:
            # not random
            query = "SELECT id, output, emotion, score FROM outputs WHERE emotion = '%s' ORDER BY score DESC LIMIT 1" % emotion

          output = self.cur.execute(query)
          output = list(self.cur.fetchone())

        else:
          output = None

        return output

    def save(self, input:str, rb_output:List, emotion:str):
        # save conversation as dict for grading

        # get correct category using emotion
        for key, value in self.categories.items():
          for x in value:
            if x == emotion:
              category = key
        conversation = {"conv_id": self.conv_id, "input": input, "rb": rb_output, "pnn": category}
        self.memory.append(conversation)

    def grade(self):
        # grade previous response using current conversation
        sentiment = self.memory[self.conv_id]['pnn']
        if len(self.memory) > 1:
            prev_conv = self.memory[self.conv_id - 1]
            prev_sentiment = prev_conv['pnn']

            change = prev_sentiment + "-" + sentiment
            print("conversation-change: ", change)
            grade = self.grading[change]
            # grade the score of the previous response in the database
            if prev_sentiment != "neu":
                prev_conv['rb'][3] = prev_conv['rb'][3] + grade
                self.update_db(prev_conv['rb'])

        self.conv_id += 1

    def update_db(self, response:List):
        # update the correct db output with the new score
        query = "UPDATE outputs SET score = %s WHERE id = %s" % (response[3], response[0])
        self.cur.execute(query)

    def reset_score(self):
        # reset all scores of db
        query = "UPDATE outputs SET score = 0"
        self.cur.execute(query)

    def reset_memory(self):
        # reset memory of class
        self.memory.clear()

    def forward(self, text:str) -> str:
        # return response.
        emotion = self.check_emotion(text)
        rb_output = self.get_output(emotion)
        self.save(text, rb_output, emotion)
        self.grade()

        if rb_output == None:
            return None

        else:
            return rb_output[1]
