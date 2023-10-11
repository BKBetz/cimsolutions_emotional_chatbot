"""Starting main.py for the first time may take some time because it needs to import all models"""

from transformers import BlenderbotSmallForConditionalGeneration, AutoModelForSeq2SeqLM
from transformers import AutoTokenizer, RobertaTokenizer
import torch
from torch import cuda
from ed_model.RobbertModel import RobbertModel
from cb.Chatbot import Chatbot
from cb.Translators import Translators

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

robbert = RobbertModel(model, tokenizer, device)
chatbot = Chatbot(blenderbot, bb_tokenizer)
transaltor = Translators(tokenizer_en, tokenizer_nl, model_en, model_nl)