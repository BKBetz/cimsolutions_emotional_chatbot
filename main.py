from transformers import RobertaTokenizer
import torch
from torch import cuda
from ed_model.RobbertModel import RobbertModel

device = 'cuda' if cuda.is_available() else torch.device('cpu')

# retrieve robbert tokenizer
tokenizer = RobertaTokenizer.from_pretrained("pdelobelle/robbert-v2-dutch-base", truncation=True, do_lower_case=True)

ed_path = "ed_model/robbert_model.pth"
model = torch.load(ed_path, map_location=torch.device('cpu'))
model.eval()

robbert = RobbertModel(model, tokenizer, device)