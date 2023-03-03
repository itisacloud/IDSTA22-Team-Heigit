from elasticsearch import Elasticsearch, helpers


class elasticSearchConnection:
    def __init__(self, host:str, port:str, kwargs:dict={}):
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

    def write(self, index:str, document: dict):
        self.client.index(index, document)

    def createIndex(self, index:str):
        body = {"mappings": {
            "properties": {
                "text": {"type": "text"},
                "user": {"type": "unsigned_long"},
                "timestamp": {"type": "date"},
                "NAME_0": {"type": "keyword"},
                "NAME_1": {"type": "keyword"},
                "NAME_2": {"type": "keyword"},
                "NAME_3": {"type": "keyword"},
                "enities": {
                    "properties": {
                        "word": {"type": "keyword"},
                        "type": {"type": "keyword"}
                    }
                },
                "sentiment": {
                    "properties": {
                        "sentiment_label": {"type": "keyword"},
                        "sentiment_value": {"type": "float"}
                    }
                }
            }
        }
        }
        self.client.indices.create(index=index, body=body)

    def bulkImport(self, index: str, fp: str, chunk_size: int = 1000):
        from elasticsearch import helpers
        import json
        if not self.client.indices.exists(index):
            self.createIndex(index)
        with open(fp) as inf:
            docs = json.load(inf)
        chunks = [docs[i:i + chunk_size] for i in range(0, len(docs), chunk_size)]
        for chunk in chunks:
            helpers.bulk(self.client, chunk, index=index)
        self.client.indices.refresh(index=index)
