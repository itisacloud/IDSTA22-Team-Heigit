import argparse
import json

from preprocess import preprocess
from process import process

def readConfig(fp:str)->dict:
    import yaml
    with open(fp, "r") as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    return config


    parser = argparse.ArgumentParser()

    parser.add_argument("command",
                        action="store",
                        default=None,
                        choices=["preprocess","process","full","full+bulk","api","bulk"],)

    parser.add_argument("-c","--config",
                        action="store",
                        default="default.config",
                        required=True
                        )

    args = parser.parse_args()

    config = readConfig(args.config)

    if args.command == "preprocess":
        preprocess(config)
    if args.command == "process":
        process(config)

    if args.command == "api":
        import uvicorn
        uvicorn.run("main:app")


    if args.command == "bulk":
        from connections import elasticSearchConnection as es
        with es(**config["elastic"]) as conn:
            conn.bulkImport(config["process"]["indexName"],config["bulk"]["filepath"])

    if args.command == "full":
        preprocess(config)
        process(config)
        import uvicorn
        uvicorn.run("main:app")

    if args.command == "full+bulk":
        from connections import elasticSearchConnection as es
        with es(**config["elastic"]) as conn:
            conn.bulkImport(config["process"]["indexName"], config["bulk"]["filepath"])
        import uvicorn
        uvicorn.run("api:app")








