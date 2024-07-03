import os
import json
import shutil
import numpy as np

def get_yolo_detection(coco_file, detection_class):
    # Create the output folders
    dir_detection_name = "temp/yolo_detection"

    # Swap key and value in desired detection class
    detection_class = {v: k for k, v in detection_class.items()}

    # check if the detection directory exists, if not create it. if so, delete the directory and create a new one
    if os.path.exists(dir_detection_name): # detection directory
        shutil.rmtree(dir_detection_name)
    os.makedirs(dir_detection_name, exist_ok=True)

    # Access and Get Information in json File
    with open (coco_file, 'r') as coco:
        coco = json.load(coco)
    
    # Get all of information from json file
    annotations = coco['annotations']       # Annotation
    images = coco['images']                 # images
    annotation_categories = {category["id"]: category["name"] for category in coco["categories"]}   # Categories dict
    img_width = images[0]["width"]          # Images width
    img_height = images[0]["height"]        # Images height

    # Create blank text file for detection and segmentation based on all images
    for img_text in images:
        text_file_name = f'{img_text['file_name'].split('/')[5].split('.')[0]}.txt'
        d_text = os.path.join(dir_detection_name, text_file_name)
        with open (d_text, 'a+') as input_d_text:
            input_d_text.write('')

    # Get Coco detection, normalize, turn into yolo
    for detection in annotations:
        if len(detection['segmentation']) == 0:
            bbox = detection['bbox']                # Get detection bounding box (x y w h)
            bbox = [max(0, val) for val in bbox]    # check if any of the bbox values are negative, then set to 0
            box = np.array(bbox, dtype=np.float64)
            box[:2] += box[2:] / 2                  # change left bottom to center bbox point
            box[[0, 2]] /= img_width                # Normalize the x
            box[[1, 3]] /= img_height               # Normalize the y
            converted_detection = ' '.join([f'{val:.6f}' for val in box.tolist()])  # Change the bbox value to string
            # Write the string into desired detection text file 
            writing = f'{dir_detection_name}/{images[detection['image_id']-1]['file_name'].split('/')[5].split('.')[0]}.txt'
            with open(writing, 'a+') as write_txt:
                write_txt.write(f'{ detection_class[annotation_categories[detection['category_id']]] } {converted_detection}\n')
        else:
            continue



file = "coco_file.json"
detection_class = {0:'pothole', 1:'alligator_crack', 2:'longitudinal_crack', 3:'lateral_crack', 4:'puddle'}
get_yolo_detection(file, detection_class)



# json file that used to convert is from images that has same width and height
# file images name that contain used to this script is "<project>/<province>/<road>/<road_segment>/images/<image_name>.jpg"
# bbox value is [x y w h]
# Result on this script is in temp/yolo_detection, the text file contain is in yolo format (example: 4 0.112271 0.214778 0.148135 0.119704)
# 4 is the from detection_class, 0.112271 0.214778 0.148135 0.119704 is the bbox in normalized value
# the script can handle more than one detection in one image
# Make sure the image and json file has same width and height, and structure tree on your json file is fit with the script