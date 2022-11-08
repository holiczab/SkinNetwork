import base64
from flask import Flask, request,Response
from load import *  # type: ignore
from ai.model import do_inference
import json

app = Flask(__name__)


@app.route("/predict", methods=["GET", "POST"])
def predict():
    
    headers = request.headers
    img_data = request.files["image"]
    pred_str, class_prob = do_inference(img_data,headers)
    
    body = json.dumps({"prediction":pred_str,"probability":class_prob})
    response = Response(body, content_type="application/json",headers={"success": True})
    
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)
