import numpy as np
import os
import shutil
import xml.etree.ElementTree as ET

def get_yolo_detection(xml_folder, detection_class):
    # Create the necessary folders variable
    dir_detection = f'your_folder_path/{xml_folder}'
    dir_detection_name = f'temp/detection'

    # check if the detection directory exists, if not create it. if so, delete the directory and create a new one
    if os.path.exists(dir_detection_name): # detection directory
        shutil.rmtree(dir_detection_name)
    os.makedirs(dir_detection_name, exist_ok=True)

    # Swap key and value in desired detection class
    detection_class = {v: k for k, v in detection_class.items()}

    # Access, Get, and Store Information in xml File
    xml_dict = {}
    for info in os.listdir(dir_detection):
        # Access the xml file
        tree = ET.parse(f'{dir_detection}/{info}')
        root = tree.getroot()
        # Get the information
        filename = root.find('filename').text
        size = root.find('size')                        # Information 1
        width = size.find('width').text
        height = size.find('height').text
        xml_dict.update({f'{filename.split('.')[0]}': []}) # Create the blank keys to handle posibility of multiple detection
        for img_object in root.findall('object'):       # Information 2
            detect_id = img_object.find('name').text
            b_box = img_object.find('bndbox')           # Information 3
            x_min = b_box.find('xmin').text
            x_max = b_box.find('xmax').text
            y_min = b_box.find('ymin').text
            y_max = b_box.find('ymax').text
            # Get all extracted value from xml file to dictionary
            xml_dict[f'{filename.split('.')[0]}'].append([width, height, detect_id, x_min, y_min, x_max, y_max])

    # Create blank text file for detection and segmentation based on all images
    for txt_file in xml_dict.keys():
        text_name = f'{txt_file}.txt'
        d_text = os.path.join(dir_detection_name, text_name)
        with open (d_text, 'a+') as input_text:
            input_text.write('')

    # Get detection value, normalize, turn into yolo
    for detection in xml_dict:
        if len(xml_dict[detection]) != 0:
            for detect in xml_dict[detection]:
                # Get detection bounding box (x_min y_min x_max y_max)
                width = int(detect[0])
                height = int(detect[1])
                detection_class_id = detect[2]
                bbox = [float(x) for x in detect[3:]]
                bbox = [max(0, val) for val in bbox]    # check if any of the bbox values are negative, then set to 0
                bbox = [bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]]     # Change the list value from x_min y_min x_max y_max to x y w h
                bbox[2] = min(bbox[2], width) # check if x_max value  more than width, then set to width value
                bbox[3] = min(bbox[3], height) # check if y_max value  more than height, then set to height value
                box = np.array(bbox, dtype=np.float64)
                box[:2] += box[2:] / 2                  # change left bottom to center bbox point
                box[[0, 2]] /= width                    # Normalize the x
                box[[1, 3]] /= height                   # Normalize the y
                converted_detection = ' '.join([f'{val:.6f}' for val in box.tolist()])  # Change the bbox value to string
                # Write the string into desired detection text file 
                write = f'{dir_detection_name}/{detection}.txt'
                with open(write, 'a+') as write_txt:
                    write_txt.write(f'{str(detection_class[detection_class_id])} {converted_detection}\n')
        else:
            continue



folder = 'your_folder_path'
detection_class = {0:'D40', 1:'D20', 2:'D00', 3:'D10', 10:'Repair', 11:'Block crack', 12:'D43', 13:'D44', 14:'D01', 15:'D11', 16:'D50', 17:'D0w0'}
get_yolo_detection(folder, detection_class)



# Please check on dir_detection variable path with the xml file folder path before run the script
# the example of xml file is ".xml" to understand access script with the xml file
# Result on this script is in temp/yolo_detection, the text file contain is in yolo format (example: 4 0.112271 0.214778 0.148135 0.119704)
# 4 is the from detection_class, 0.112271 0.214778 0.148135 0.119704 is the bbox in normalized value
# the script can handle more than one detection in one image