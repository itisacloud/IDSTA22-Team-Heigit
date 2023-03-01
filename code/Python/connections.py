from elasticsearch import Elasticsearch, helpers

class elasticSearchConnection:
    def __init__(self,host,port,kwargs={}):
        self.host = host
        self.port = port
        self.kwargs = kwargs

    def __enter__(self):
        self.client = Elasticsearch(f"{self.host}:{self.port}",
                                   **self.kwargs
                                    )
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
    def write(self,index,fid,document:dict):
        self.client.index(index, document)




