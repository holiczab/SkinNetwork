from pathlib import Path
from typing import Dict, List
from PIL import Image
import numpy as np
import onnxruntime as ort  # type: ignore

from utils import *

INPUT_SHAPE: List[int] = [640, 640, 3]  # yolov5l input size
ONNX_PATH: Path = Path(RESOURCES_PATH / "small.onnx")
OBJECTNESS_CONFIDENCE_THRESHOLD: int = 0.5
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
    img = np.transpose(img,(2,0,1))
    img = img[None,:]
    
    return img

def convert_encoded_image(img_data: str) -> np.ndarray:
    
    pil_img = Image.open(img_data).convert("RGB")
    img = np.asarray(pil_img, dtype=np.float32)
    return img
    

def predict(img: np.ndarray) -> np.ndarray:

    ort_pred = ort_session.run(output_names=None, input_feed={"images": img})
    return ort_pred[0]


def postprocess_prediction(ort_pred: np.ndarray) -> str:
    #yolov5 output last dimension - [xywh,objectness,class confidences]
    pred = ort_pred.squeeze()
    pred = pred[pred[:,5] > OBJECTNESS_CONFIDENCE_THRESHOLD]
    class_confidences = pred[:,5:]
    max_indices = np.argmax(class_confidences,axis=1)
    
    class_num = np.argmax(ort_pred, axis=0)
    class_str = CLASS_MAPPING[class_num]
    return class_str


def do_inference(img_data: str,headers: Dict[str,str]) -> str:

    img = preprocess_img(img_data,headers)    
    network_prediction = predict(img)
    class_str = postprocess_prediction(network_prediction)
    return class_str
