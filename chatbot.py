from transformers import BlenderbotSmallForConditionalGeneration
from transformers import AutoTokenizer


class ChatbotModel:
    def __init__(self):
        self.model = BlenderbotSmallForConditionalGeneration.from_pretrained("facebook/blenderbot_small-90M", add_cross_attention=False)
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/blenderbot_small-90M")

    def response(self, text):
        # TODO: edit chatbot response, remove "_start_ , _end_" from reply
        inputs = self.tokenizer([text], return_tensors="pt")
        reply = self.model.generate(**inputs)

        return reply
