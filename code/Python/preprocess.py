import re
def clean(text: str) -> str:
    text.replace("\n", " ")
    new_text = []
    it_main = iter(text.split(" "))

    for chunk_main in it_main:
        chunk_main = 'http' if chunk_main.startswith('http') else chunk_main  # remove links and replace with http
        new_chunk = []
        it = iter(re.findall(r"[\w']+|[.,!?;/@_-]", chunk_main))
        for chunk in it:  # keep punktuation

            if chunk == "@":
                try:
                    chunk += it.__next__()
                except:
                    pass
            chunk = '@user' if chunk.startswith('@') and len(chunk) > 1 else chunk  # standardize users
            new_chunk.append(chunk)
        new_text.append("".join(new_chunk))
    return " ".join(new_text)

from translator import Translator
from rdata_to_df import rdata_to_df
from geo import GeoCoder, get_geo_from_id
from tqdm import tqdm
def preprocess(config):
    fp= config["preprocess"]["rawTweetsPath"]
    fp_output= config["preprocess"]["preprocessedPath"]
    fp_aoi= config["preprocess"]["aoiPath"]
    cols = config["preprocess"]["columns"]
    df = rdata_to_df(fp)
    translator = Translator()
    tqdm.pandas()
    df["clean"] = df["text"].apply(clean)
    df['trans'] = df.progress_apply(lambda x: translator.translate(x.clean, x.lang), axis=1)

    geoCoder=GeoCoder(fp=fp_aoi, cols=cols)
    #df["geomtry"] = df.apply(lambda x: get_geo_from_id(x.place_id))
    df[cols] = df.progress_apply(lambda x: geoCoder.intersect(x.geometry),result_type='expand',axis=1)
    df.to_pickle(fp_output, index=False)




