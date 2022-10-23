from flask import Flask, request
from load import *  # type: ignore

from ai.model import do_inference

app = Flask(__name__)


@app.route("/predict/", methods=["GET", "POST"])
def predict():

    imgData: str = request.get("image", type=str)
    pred_str: str = do_inference(imgData)

    return pred_str


if __name__ == "__main__":
    app.run(debug=True, port=8080)
