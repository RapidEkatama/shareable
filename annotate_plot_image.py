import cv2
import matplotlib.pyplot as plt

def annotate_plot_image(source_path):
    # Get the image path and annotate path
    img_path = f'your_image_path/{source_path.split(".")[0]}.jpg'
    annotate_crack_path = f'your_annotation_YOLO_textfile_path/{source_path}'
    img = cv2.imread(img_path, -1)
    img_print = img[:, :, ::-1]

    height, width, channel = img.shape

    # Breakdown the crack annotate into dictionary
    annotations = []
    with open(annotate_crack_path, 'r') as crack_file:
        crack_lines = crack_file.readlines()

    for line in crack_lines:
        crack = list(map(float, line.split()))
        class_id = int(crack[0])
        x_center, y_center, bbox_width, bbox_height = crack[1:]

        # Convert YOLO format to bounding box coordinates
        x_min = int((x_center - bbox_width / 2) * width)
        y_min = int((y_center - bbox_height / 2) * height)
        x_max = int((x_center + bbox_width / 2) * width)
        y_max = int((y_center + bbox_height / 2) * height)

        # Store the annotation in the list
        annotations.append({'class_id': class_id, 
                            'x_min': x_min,
                            'y_min': y_min,
                            'x_max': x_max,
                            'y_max': y_max})

    # Define color and label dictionary
    color_label_dict = {0: {'color': (255, 0, 0), 'label': 'pothole'},
                        1: {'color': (0, 255, 0), 'label': 'alligator_crack'},
                        2: {'color': (0, 0, 255), 'label': 'longitudinal_crack'},
                        3: {'color': (255, 128, 0), 'label': 'lateral_crack'}}

    # Plot the annotations
    for annotation in annotations:
        class_id = annotation['class_id']
        x_min = annotation['x_min']
        y_min = annotation['y_min']
        x_max = annotation['x_max']
        y_max = annotation['y_max']

        color = color_label_dict[class_id]['color']
        label = color_label_dict[class_id]['label']

        # Draw the bounding box and label on the image
        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color, 2)
        cv2.putText(img, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    
    # Save the image with annotations
#    output_path = f'your_output_image_with_annotation_path/{source_path.split(".")[0]}.jpg'
#    cv2.imwrite(output_path, img)

    # Display the image with annotations
    plt.axis('off')
    plt.title(source_path.split('.')[0])
    plt.imshow(img_print)



annotate_plot_image('yolo_annotation.txt')



# this script will plot the images with its damages annotation
# Please check on img_path and annotate_crack_path path with the annotation file and image path before run the script
# annotation file in YOLO text file
# Make sure your image name and YOLO file name are the same