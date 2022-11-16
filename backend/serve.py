import traceback
from flask import Flask, request,Response
from ai.model import do_inference
import json
from PIL import Image # type: ignore
from utils import forge_fail_response
app = Flask(__name__)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    
    json_data = request.json
    headers = request.headers
    
    try:
        pred_str, class_prob = do_inference(json_data,headers)
    except Exception as e:
        print(traceback.format_exc())
        return forge_fail_response(str(e))
    
    body = json.dumps({"prediction":pred_str,"probability":class_prob})
    response = Response(body, content_type="application/json",headers={"success": True})
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)
