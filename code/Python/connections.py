from elasticsearch import Elasticsearch, helpers

class elasticSearchConnection():
    def __int__(self,host,user:str,password:str):
        es = Elasticsearch(host,)

    def auth(self)->bool:
    def write(self,index,fid,document:dict)->bool:
        es.index(index,document)


