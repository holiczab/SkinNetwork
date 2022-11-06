from pprint import pprint
import requests as rqs # type: ignore
import utils

if __name__ == "__main__":

    fh = {"image":open(utils.BACKEND_ROOT/"resources"/"im.png","rb")}
    
    resp = rqs.get("http://127.0.0.1:8080/predict",files=fh,headers={"image-type": "encoded"})
     
    print(resp.headers)
    print(resp.text)
    print(resp.json)
