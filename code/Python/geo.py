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
        return self.df[self.df.intersects(geom)][self.cols]

def get_geo_from_id(id):
    url =  f"https://api.twitter.com/1.1/geo/id/{id}.json"
    json.loads(urllib.request.urlopen(url).read())











