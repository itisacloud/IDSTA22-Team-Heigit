
from transformers import pipeline
from scipy.special import softmax

class sentimentResult():
    def __init__(self, text:str, result:[dict]):
        self.text = text
        self.sentiment = result[0]['score']
        self.sentiment_ = result[0]['label']
class SentimentModel:
    def __init__(self, model:str):
        self.model = model
        self.MODEL = pipeline("sentiment-analysis", model=model, tokenizer=model)

    def apply_pipeline(self, text: str) -> sentimentResult:
        result = self.MODEL(text)
        print(result)
        return sentimentResult(text, result)


if __name__ == "__main__":
    sent = SentimentModel('cardiffnlp/twitter-roberta-base-sentiment-latest')

    for test in ["Thats Awesome!!!","i hate you","fuck that","This paper is a scientic breakthrough","three plus four is seven"]:
        sent.apply_pipeline(test)
