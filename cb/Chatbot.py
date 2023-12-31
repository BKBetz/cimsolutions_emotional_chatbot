""" This class contains the pre-trained blenderbot. Using it's tokenizer, it returns a given input."""


class Chatbot:
    def __init__(self, model, tokenizer) -> None:
        self.model = model
        self.tokenizer = tokenizer

    def convert(self, text: str):
        # convert to reply_ids which in return provide a output from the cb
        inputs = self.tokenizer([text], return_tensors="pt")
        reply_ids = self.model.generate(**inputs)
        return reply_ids

    def clean_string(self, text: str) -> str:
        # using split. the sentence will always be in the same place. This way u can easily retrieve it

        splitted_text = text.split('_')
        text = splitted_text[4]

        return text

    def response(self, text: str) -> str:
        # generate clean response from cb
        reply_ids = self.convert(text)
        output = self.tokenizer.batch_decode(reply_ids)
        response = self.clean_string(output[0])
        return response
