from pathlib import Path
from typing import List

import imageio
import numpy as np
import onnxruntime as ort  # type: ignore

from utils import RESOURCES_PATH

INPUT_SHAPE: List[int] = [640, 640]  # yolov5l input size
ONNX_PATH: Path = RESOURCES_PATH / "yolov5l_ham10000.onnx"

CLASS_MAPPING: dict[int, str] = {
    0: "dont know / healthy",
    1: "Melanocytic nevi",
    2: "Melanoma",
    3: "Benign keratosis-like lesion",
    4: "Basal cell carcinoma",
    5: "Actinic keratose",
    6: "Vascular lesion",
    7: "Dermatofibroma",
}


def create_ort_session(model_onnx_path: Path):
    assert model_onnx_path.exists()
    ort_sess = ort.InferenceSession(model_onnx_path)
    return ort_sess


global ort_session
ort_session = create_ort_session(ONNX_PATH)


def convert_image(img_data: str) -> np.ndarray:
    b_img_data = bytes(img_data, encoding="utf-8")
    io_img = imageio.imread(b_img_data)
    img = np.asarray(io_img, dtype=np.float32)
    return img


def preprocess_img(img_data: str) -> np.ndarray:

    img: np.ndarray = convert_image(img_data)
    img = np.resize(img, INPUT_SHAPE)
    return img


def predict(img: np.ndarray) -> np.ndarray:

    ort_pred = ort_session.run(output_names=None, input_names={"image_input": img})
    return ort_pred[0]


def postprocess_prediction(ort_pred: np.ndarray) -> str:
    class_num = np.argmax(ort_pred, axis=1)
    class_str = CLASS_MAPPING[class_num]
    return class_str


def do_inference(img_data: str) -> str:

    img = preprocess_img(img_data)
    network_prediction = predict(img)
    class_str = postprocess_prediction(network_prediction)
    return class_str
