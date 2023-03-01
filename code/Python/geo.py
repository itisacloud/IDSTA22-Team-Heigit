import geopandas as gpd
from shapely import Geometry
import requests
import urllib
import json
class GeoCoder:
    def __init__(self,fp,cols,DRIVER="geoJSON",):
        self.path = fp
        self.cols = cols
        self.DRIVER = DRIVER
        self.df = gpd.read_file(fp,DRIVER=DRIVER)
    def intersect(self,geom:Geometry):
        try:
            res = self.df[self.df.intersects(geom)][self.cols]
            res = [res[i].tolist()[0] for i in self.cols]
        except:
            res = ["None" for i in self.cols]
        return res

def get_geo_from_id(id):
    url =  f"https://api.twitter.com/1.1/geo/id/{id}.json"
    json.loads(urllib.request.urlopen(url).read())













