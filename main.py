"""Starting main.py for the first time may take some time because it needs to import all models"""

from transformers import BlenderbotSmallForConditionalGeneration, AutoModelForSeq2SeqLM
from transformers import AutoTokenizer, RobertaTokenizer
import torch
from torch import cuda
import sqlite3 as sql
from ed_model.RobbertModel import RobbertModel
from cb.Chatbot import Chatbot
from cb.Translators import Translators
from ed_output.RetrievalOutput import RetrievalOutput

device = 'cuda' if cuda.is_available() else torch.device('cpu')

# retrieve robbert tokenizer and model
tokenizer = RobertaTokenizer.from_pretrained("pdelobelle/robbert-v2-dutch-base", truncation=True, do_lower_case=True)

ed_path = "ed_model/robbert_model.pth"
model = torch.load(ed_path, map_location=torch.device('cpu'))
model.eval()

# retrieve pre-trained cb
blenderbot = BlenderbotSmallForConditionalGeneration.from_pretrained("facebook/blenderbot_small-90M", add_cross_attention=False)
bb_tokenizer = AutoTokenizer.from_pretrained("facebook/blenderbot_small-90M")

# import translator models and tokenizers
tokenizer_en = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-nl-en")
tokenizer_nl = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-nl")

model_en = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-nl-en")
model_nl = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-nl")

# connect with database
db_path = "ed_output/ed_outputs.db"
conn = sql.connect(db_path)
cur = conn.cursor()

robbert = RobbertModel(model, tokenizer, device)
chatbot = Chatbot(blenderbot, bb_tokenizer)
transaltor = Translators(tokenizer_en, tokenizer_nl, model_en, model_nl)
rbo = RetrievalOutput(conn, cur, 0.9, robbert)

"""with all classes made and created..a final class will be made which gives a output"""

""" This class creates a conversation agent that can be used to creat small conversations where an emotion is being detected.
It combines the chatbot output with the retrieval based output (could be made cleaner with nlp)"""


class ConversationAgent:

    def __init__(self, chatbot, translators, rbo):
        self.cb = chatbot
        self.translators =  translators
        self.rbo = rbo

    def get_rbo(self, text:str) -> str:
        # get output from retrieval based system
        rb_output = self.rbo.forward(text)
        return rb_output

    def cb_response(self, text:str) -> str:
        # get output from chatbot
        en_text = self.translators.translate(text, "en")
        cb_text = self.cb.response(en_text)
        nl_text = self.translators.translate(cb_text, "nl")
        return nl_text

    def combine_outputs(self, cb_output:str, retrieval_output:str) -> str:
        # combine the two outputs
        combined = cb_output + " " + retrieval_output
        return combined

    def reset_rbo(self):
        # reset memory of retrieval based system
        self.rbo.reset_score()
        self.rbo.reset_memory()

    def forward(self, text: str) -> str:
        # get response
        cb_output =  self.cb_response(text)
        retrieval_output = self.get_rbo(text)
        combined = self.combine_outputs(cb_output, retrieval_output)
        if retrieval_output ==  None:
            return cb_output
        else:
            return combined


conv_agent = ConversationAgent(chatbot, transaltor, rbo)

"create a small while loop that allows you to have a small conversation with the chatbot"

# uncomment to reset memory stats
# conv_agent.reset_rbo()

x = 0
while x < 10:
    user_input = input("enter your text here: ")
    if user_input == "exit":
        break
    else:
        response = conv_agent.forward(user_input)
        print("response: ", response)
        x += 1
