import json
import traceback

import yaml

from flask import Flask, Response, request

from ai.model import do_inference
from utils import forge_fail_response

app = Flask(__name__)


@app.route("/predict", methods=["GET", "POST"])
def predict():

    json_data = request.json
    headers = request.headers

    try:
        pred_str, class_prob = do_inference(json_data, headers)
    except Exception as e:
        print(traceback.format_exc())
        return forge_fail_response(str(e))

    body = json.dumps({"prediction": pred_str, "probability": class_prob})
    response = Response(
        body, content_type="application/json", headers={"success": True}
    )
    return response


if __name__ == "__main__":
    with open("startup_cfg.yaml", "r") as cfg_yaml:
        try:
            cfg = yaml.safe_load(cfg_yaml)
        except yaml.YAMLError as exc:
            print(exc)
    
    app.run(host=cfg["host"], debug=cfg["debug"], port=cfg["port"])
