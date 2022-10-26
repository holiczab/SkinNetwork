from pathlib import Path
from typing import Dict, List
from PIL import Image
import numpy as np
import onnxruntime as ort  # type: ignore

from utils import RESOURCES_PATH

INPUT_SHAPE: List[int] = [640, 640]  # yolov5l input size
ONNX_PATH: Path = Path("/Users/zsomborcsurilla/Documents/elte_msc/2022_osz/halszte/SkinNetwork/backend/resources/yolov5l_ham10000.onnx")

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
    ort_sess = ort.InferenceSession(str(model_onnx_path))
    return ort_sess


global ort_session
ort_session = create_ort_session(ONNX_PATH)


def preprocess_img(img_data: str,headers: Dict[str,str]) -> np.ndarray:
    
    if headers["Image-Type"] == "encoded" :
        img: np.ndarray = convert_encoded_image(img_data)
        
    img = np.resize(img, INPUT_SHAPE)
    return img

def convert_encoded_image(img_data: str) -> np.ndarray:
    
    pil_img = Image.open(img_data)
    img = np.asarray(pil_img, dtype=np.float32)
    return img
    

def predict(img: np.ndarray) -> np.ndarray:

    ort_pred = ort_session.run(output_names=None, input_feed={"onnx::Reshape_0": img})
    return ort_pred[0]


def postprocess_prediction(ort_pred: np.ndarray) -> str:

    class_num = np.argmax(ort_pred, axis=0)
    class_str = CLASS_MAPPING[class_num]
    return class_str


def do_inference(img_data: str,headers: Dict[str,str]) -> str:

    img = preprocess_img(img_data,headers)
    network_prediction = predict(img)
    class_str = postprocess_prediction(network_prediction)
    return class_str
