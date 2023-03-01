from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification

class entityResult():
    def __init__(self, text:str, result:[dict]):
        self.text = text
        self.result = result
    def format(self):
        return {"enities":[{"type":res["entity"],"word":self.text[int(res["start"]):int(res["end"])].lower()} for res in self.result]}

class entityModel:
    def __init__(self, model:str):
        self.model = model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)
        self.MODEL = AutoModelForTokenClassification.from_pretrained(self.model)
        self.MODEL = pipeline("ner", model=self.MODEL, tokenizer=self.tokenizer)

    def apply_pipeline(self, text: str) -> entityResult:
        result = self.MODEL(text)
        return entityResult(text,result)


if __name__ == "__main__":
    sent = entityModel('Jean-Baptiste/roberta-large-ner-english')
    for test in ["Thats Awesome!!!","i hate you","fuck that","This paper is a scientic breakthrough","three plus four is seven","Jeff Bezos is the CEO of Amazon","Apple is the most valuable company in the world for no reason"]:
        res = sent.apply_pipeline(test)

