from pathlib import Path
from typing import Dict, List, Tuple
from PIL import Image # type: ignore
import numpy as np
import onnxruntime as ort  # type: ignore
from utils import * # type: ignore

INPUT_SHAPE: List[int] = [640, 640, 3]  # yolov5l input size
ONNX_PATH: Path = Path(RESOURCES_PATH / "small.onnx") # type: ignore 

OBJECTNESS_CONFIDENCE_THRESHOLD: float = 0.8
CLASS_PROBABILITY_THRESHOLD: float = 0.8
CLASS_MAPPING: dict[int, str] = {
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


def preprocess_img(img_data: str,headers: Dict[str,str]) -> np.ndarray:
    
    if headers["Image-Type"] == "encoded" :
        img: np.ndarray = convert_encoded_image(img_data)
        
    img = np.resize(img, INPUT_SHAPE)
    img = np.transpose(img,(2,0,1))
    img = img[None,:]
    img = (img - np.min(img)) / (np.max(img) - np.min(img))
    return img

def convert_encoded_image(img_data: str) -> np.ndarray:
    
    pil_img = Image.open(img_data).convert("RGB")
    img = np.asarray(pil_img, dtype=np.float32)
    return img

def predict(img: np.ndarray) -> np.ndarray:
    ort_pred = ort_session.run(output_names=None, input_feed={"images": img})
    return ort_pred[0]


def postprocess_prediction(ort_pred: np.ndarray) -> Tuple[str,float]:
    #yolov5 output last dimension - [xywh,objectness,class confidences]
    pred = ort_pred.squeeze()
    pred = pred[pred[:,5] > OBJECTNESS_CONFIDENCE_THRESHOLD]

    if len(pred) == 0:
        return ("dont know",0.)
    
    class_probits = pred[:,5:]

    box_max_indices = np.argmax(class_probits,axis=1)
    box_max_prob_values = class_probits[range(len(class_probits)),box_max_indices]
    
    max_prob_index = np.argmax(box_max_prob_values)
    max_prob_class_index = box_max_indices[max_prob_index] 
    max_prob_val = box_max_prob_values[max_prob_index]
    
    if max_prob_val < CLASS_PROBABILITY_THRESHOLD:
        return ("dont know",0.)
    
    class_str = CLASS_MAPPING[int(max_prob_class_index)]

    return (class_str,float(max_prob_val))


def do_inference(img_data: str,headers: Dict[str,str]) -> Tuple[str,float]:

    img = preprocess_img(img_data,headers)
    prediction = predict(img)
    class_str,prob = postprocess_prediction(prediction)
    return (class_str,prob)
