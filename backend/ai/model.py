import base64
import json
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import onnxruntime as ort  # type: ignore
from PIL import Image  # type: ignore

from utils import *  # type: ignore

INPUT_SHAPE: List[int] = [640, 640, 3]  # yolov5l input size
ONNX_PATH: Path = Path(RESOURCES_PATH / "small.onnx")  # type: ignore

OBJECTNESS_CONFIDENCE_THRESHOLD: float = 0.8
CLASS_PROBABILITY_THRESHOLD: float = 0.8
CLASS_MAPPING: Dict[int, str] = {
    0: "Melanocytic nevi",
    1: "Melanoma",
    2: "Benign keratosis-like lesion",
    3: "Basal cell carcinoma",
    4: "Actinic keratose",
    5: "Vascular lesion",
    6: "Dermatofibroma",
    7: "dont know",
}


def create_ort_session(model_onnx_path: Path):
    assert model_onnx_path.exists()
    ort_sess = ort.InferenceSession(str(model_onnx_path))
    return ort_sess


global ort_session
ort_session = create_ort_session(ONNX_PATH)


def preprocess_img(json_data: str, headers) -> np.ndarray:
    if headers["client"] == "desktop":

        body_dict = json.loads(json_data)["files"]
        img_array = json.loads(body_dict["image"])
        img = np.asarray(img_array, dtype=np.float32)

    elif headers["client"] == "mobile":
        temp = json.dumps(json_data)
        body_dict = json.loads(temp)

        image_png = base64.b64decode(json.loads(body_dict)["image"])
        pil_img = Image.open(BytesIO(image_png)).convert("RGB")
        img = np.asarray(pil_img, dtype=np.float32)

    img = np.resize(img, INPUT_SHAPE)
    img = np.transpose(img, (2, 0, 1))
    img = img[None, :]
    img = (img - np.min(img)) / (np.max(img) - np.min(img))
    return img


def predict(img: np.ndarray) -> np.ndarray:
    ort_pred = ort_session.run(output_names=None, input_feed={"images": img})
    return ort_pred[0]


def postprocess_prediction(ort_pred: np.ndarray) -> Tuple[str, float]:
    
    # yolov5 output last dimension - [xywh, objectness score, class confidences]
    pred = ort_pred.squeeze()
    
    pred_objectness_filtered = pred[pred[:, 5] > OBJECTNESS_CONFIDENCE_THRESHOLD]
    print(len(pred_objectness_filtered) / len(pred) )
    if len(pred_objectness_filtered) / len(pred) < 0.1:
        return ("dont know", 0.0)

    class_probits = pred[:, 5:]

    box_max_indices = np.argmax(class_probits, axis=1)
    box_max_prob_values = class_probits[range(len(class_probits)), box_max_indices]

    max_element = np.bincount(box_max_indices).argmax()
    
    #print("bincount:",np.bincount(box_max_indices))
    best_class_prob_values = box_max_prob_values[box_max_indices == max_element]
    #print("best_class_values:",np.average(best_class_values))
    
    best_class_avg_prob = np.average(best_class_prob_values)

    class_str = CLASS_MAPPING[int(max_element)]

    return (class_str, float(best_class_avg_prob))


def do_inference(json_data: str, headers) -> Tuple[str, float]:

    img = preprocess_img(json_data, headers)
    prediction = predict(img)
    class_str, prob = postprocess_prediction(prediction)
    return (class_str, prob)
