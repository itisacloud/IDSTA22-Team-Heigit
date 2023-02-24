
from transformers import pipeline
from scipy.special import softmax

class sentimentResult():
    def __init__(self, text:str, result:[dict]):
        self.text = text
        self.sentiment = result[0]['score']
        self.sentiment_ = result[0]['label']
    def format(self):
        return {"sentiment_label":self.sentiment_,"sentiment_score":self.sentiment}


class sentimentModel:
    def __init__(self, model:str):
        self.model = model
        self.MODEL = pipeline("sentiment-analysis", model=model, tokenizer=model)

    def apply_pipeline(self, text: str) -> sentimentResult:
        result = self.MODEL(text)
        print(result)
        return sentimentResult(text, result)


if __name__ == "__main__":
    sent = sentimentModel('cardiffnlp/twitter-roberta-base-sentiment-latest')

    for test in ["Thats Awesome!!!","i hate you","fuck that","This paper is a scientic breakthrough","three plus four is seven"]:
        res = sent.apply_pipeline(test)
        print(res.sentiment,res.sentiment_)
