import base64
import json
from pathlib import Path

import numpy as np
import requests as rqs  # type: ignore
from PIL import Image  # type: ignore

import utils


def client_get_test_desktop(image_path: Path):

    pil_img = Image.open(str(image_path))
    json_data = json.dumps(np.array(pil_img).tolist())
    json_data = json.dumps({"files": {"image": json_data}})
    resp = rqs.get(
        "http://127.0.0.1:8080/predict", json=json_data, headers={"client": "desktop"}
    )

    assert resp.json() is not None
    print(resp.json())


def client_get_test_mobile(image_path: Path):
    with open(
        str(image_path), "rb"
    ) as image_file:
        image_text = image_file.read()

    json_data = json.dumps(base64.b64encode(image_text).decode("utf-8"))
    json_data = json.dumps({"image": json_data})
    resp = rqs.get(
        "http://127.0.0.1:8080/predict", json=json_data, headers={"client": "mobile"}
    )

    assert resp.json() is not None
    print(resp.json())


if __name__ == "__main__":
    print("sending vascular lesion...")
    client_get_test_desktop(utils.BACKEND_ROOT / "resources" / "vascular_lesion.jpeg")
    
    print("sending birthmark...")
    client_get_test_desktop(utils.BACKEND_ROOT / "resources" / "test_birthmark.jpeg")
    
    print("sending negative example...")
    client_get_test_desktop(utils.BACKEND_ROOT / "resources" / "test_negative.png")
