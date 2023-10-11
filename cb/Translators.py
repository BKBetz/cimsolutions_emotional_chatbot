""" This class contains both translators. Based on the given language input,
the sentence gets translated from en-nl or nl-en"""


class Translators:
    def __init__(self, en_tokenizer, nl_tokenizer, en_model, nl_model) -> None:
        self.en_model = en_model
        self.nl_model = nl_model
        self.en_tokenizer = en_tokenizer
        self.nl_tokenizer = nl_tokenizer

    def en_translate(self, text: str) -> str:
        # translate to english
        batch = self.en_tokenizer([text], return_tensors="pt")
        generated_ids = self.en_model.generate(**batch)
        translation = self.en_tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return translation

    def nl_translate(self, text: str) -> str:
        # translate to dutch
        batch = self.nl_tokenizer([text], return_tensors="pt")
        generated_ids = self.nl_model.generate(**batch)
        translation = self.nl_tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return translation

    def translate(self, text: str, language:str) -> str:
        # choose translator based on given language
        if language == "nl":
            translated = self.nl_translate(text)
        elif language == "en":
            translated = self.en_translate(text)
        else:
            translated = "Language not found"

        return translated
