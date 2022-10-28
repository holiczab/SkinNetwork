# Network Training

## Data

Download the images from [HAM10000 dataset](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DBW86T) website.
The necessary files:
- `HAM10000_images_part_1.zip`
- `HAM10000_images_part_2.zip`
- `HAM10000_metadata.tab`

Unzip and separate the images into two folders `images` and `test`. Zip the two folders `images.zip` and `test.zip`. Zipping is necessary because folders cannot be uploaded to Collab.


## Labeling

The labels are created from HAM10000_metadata.tab file. To be compatible with the label format of the YOLOv5 network, a separate `imagename.txt` file is created for every image in the dataset. Each file contains the bounding box of the whole image, since images only contain the skin lesions, the bounding boxes are set to be the whole image.

Run the `labels_to_yolo_format.py` file in the same folder as the `HAM10000_metadata.tab` file. Zip the created `labels` folder.

The `HAM10000_data.yaml` file contains the information of the classes and the train, test, and label folders filepath in Collab.

## Running network on Collab

Upload the `YOLOv5_custom_training.ipynb` file to Google Collab. Follow the instructions in the notebook.

The following files will need to be uploaded:
- `images.zip`
- `labels.zip`
- `test.zip`
- `HAM10000_data.yaml`