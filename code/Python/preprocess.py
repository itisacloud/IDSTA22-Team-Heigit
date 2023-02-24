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


def preprocess(fp:str, fp_output:str, fp_aoi:str, cols: list[str]):
    df = rdata_to_df(fp)


    translator = Translator()

    tqdm.pandas()

    # preprocessing

    df["clean"] = df["text"].apply(clean)
    df['translated'] = df.progress_apply(lambda x: translator.translate(x.clean, x.lang), axis=1)

    GeoCoder(fp=fp_aoi, cols=cols)
    df["geom"] = df.apply(lambda x: get_geo_from_id(x.place_id))
    df[cols] = df.apply(lambda x: GeoCoder.intersect(x.geom))
    df.to_csv(fp_output, index=False)

if __name__ == "__main__":
    fp = r"../../files/tweets/output.RData"
    cols = [f"NAME_{i}" for i in range(4)]
    fp_aoi = r"../../files/aoi/3_mittel.geo.json"
    fp_output = "../../files/tweets/output.csv"
    preprocess(fp,fp_output,fp_aoi,cols)


