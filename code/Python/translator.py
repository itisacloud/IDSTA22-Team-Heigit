class Translator:
    def __init__(self):
        self.MODELS = {
        }

    def translate(self, text: str, source: str) -> str:

        try:
            if source in self.MODELS.keys():
                if self.MODELS[source] is not None:
                    return self.MODELS[source](text)[0]["translation_text"]
            elif source in ["de", "uk", "ru", "en", "pl"]:
                try:
                    self.MODELS[source] = pipeline("translation", model=f"Helsinki-NLP/opus-mt-{source}-en")
                    return self.MODELS[source](text)[0]["translation_text"]
                except Exception as e:
                    self.MODELS[source] = None
        except Exception as e:
            traceback.print_exc()
            pass
        return None


if __name__ == "__test__":
    tr = Translator()
    for text in ["this is a test.@thomas_peter @günther. Das ist ein test! http:test.com", "das ist ein zweiter test",
                 "das ist ja total awesome", "this is a test", "Wie geht es dir"]:
        text = clean(text)
        print(tr.translate(text, "de"))