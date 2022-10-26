from flask import Flask, request,Response
from load import *  # type: ignore
import sys
from ai.model import do_inference
import json

app = Flask(__name__)


@app.route("/predict", methods=["GET", "POST"])
def predict():
    
    headers = request.headers

    img_data = request.files["image"]
    pred_str: str = do_inference(img_data,headers)
    
    body = json.dumps({"prediction":pred_str})
    response = Response(body, content_type="application/json",headers={"success": True})
    
    return response


if __name__ == "__main__":
    app.run(debug=True, port=8080)
