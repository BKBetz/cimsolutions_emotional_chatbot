""" This class contains the robbert model. which detects an emotion. emotions are labeled and send back to the user."""
import torch


class RobbertModel:
    def __init__(self, model, tokenizer, device) -> None:
        self.model = model
        self.tokenizer = tokenizer
        self.labels = {0: 'neutral', 1:'joy', 2:'fear', 3:'anger', 4:'sad', 5:'love', 6:"other"}
        self.device = device

    def convert(self, text: str):
        # tokenize text to make predictions
        tokenized = self.tokenizer(text)

        tt = {
        'ids': torch.tensor(tokenized['input_ids'], dtype=torch.long),
        'mask': torch.tensor(tokenized['attention_mask'], dtype=torch.long),
        }

        ids = tt['ids'].to(self.device, dtype = torch.long)
        mask = tt['mask'].to(self.device, dtype = torch.long)
        return ids, mask

    def predict(self, text: str) -> str:
        ids, mask = self.convert(text)
        output = self.model(ids.unsqueeze(0), mask.unsqueeze(0))
        emotion =  self.labels[output.logits.argmax(1).item()]

        return emotion