import os
import cv2
import numpy as np
import tensorflow as tf
import requests

# Download model if not exist
def download_model():
    url = "https://drive.google.com/uc?id=1Ml260620LIKa-OrWqdzv_z99NJKixt3W"
    output_path = "ssd_mobilenetv2_coco/saved_model.pb"

    response = requests.get(url, stream=True)

    with open(output_path, "wb") as output_file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                output_file.write(chunk)

# Explicitly specify the GPU device
physical_devices = tf.config.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

# Initialize model variable
model = None

def create_folder(output_directory):
    # Check if the folder exists
    if not os.path.exists(output_directory):
        try:
            # Create the folder if it doesn't exist
            os.makedirs(output_directory)
            print(f"LOG: Folder '{output_directory}' created successfully.")
        except OSError as e:
            print(f"LOG: Error creating folder '{output_directory}': {e}")

# Function to perform object detection and crop the image
def object_detection(input_image_path, output_directory):

    # Read the input image
    image = cv2.imread(input_image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_expanded = np.expand_dims(image_rgb, axis=0).astype(np.uint8)

    # Perform inference
    detections = model.signatures["serving_default"](tf.constant(image_expanded))

    # Extract coordinates of detected persons
    detection_classes = detections['detection_classes'][0].numpy()
    detection_boxes = detections['detection_boxes'][0]
    person_indices = tf.where(tf.equal(detection_classes, 1))[:, 0]
    person_coords = tf.gather(detection_boxes, person_indices).numpy()

    # Crop the original image based on the detected persons' coordinates
    for i, coords in enumerate(person_coords):
        ymin, xmin, ymax, xmax = coords

        # Ensure valid coordinates
        if 0 <= ymin < ymax <= image.shape[0] and 0 <= xmin < xmax <= image.shape[1]:
            if ymin - (ymin * 0.1) >= 0:
                ymin = int((ymin - (ymin * 0.1)) * image.shape[0])
            else:
                ymin = int(ymin * image.shape[0])
            
            if int((ymax + (ymax * 0.1)) * image.shape[0]) <= image.shape[0]:
                ymax = int((ymax + (ymax * 0.1)) * image.shape[0])
            else:
                ymax = int(ymax * image.shape[0])
            
            if xmin - (xmin * 0.1) >= 0:
                xmin = int((xmin - (xmin * 0.1)) * image.shape[1])
            else:
                xmin = int(xmin * image.shape[1])
            
            if int((xmax + (xmax * 0.1)) * image.shape[1]) <= image.shape[1]:
                xmax = int((xmax + (xmax * 0.1)) * image.shape[1])
            else:
                xmax = int(xmax * image.shape[1])
            
            cropped_person = image[ymin:ymax, xmin:xmax, :]

            # Check if the cropped_person array is not empty
            if not cropped_person.size == 0:
                # Save the cropped person image with correct color space conversion
                try:
                    image_name = os.path.basename(input_image_path)
                    # Save the image using cv2.imwrite()
                    cv2.imwrite(f"{output_directory}/{i + 1}_{image_name}", cropped_person)
                    print(f"LOG: Image saved successfully to '{output_directory}/{i + 1}_{image_name}'.")
                except Exception as e:
                    print(f"LOG: Error saving image: {e}")
            else:
                print(f"LOG: Warning: Cropped person {i + 1} is empty.")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python person_crop.py <input_image_folder> <output_directory>")
        sys.exit(1)

    input_image_folder = sys.argv[1]
    output_directory = sys.argv[2]
    
    if os.path.exists("ssd_mobilenetv2_coco/saved_model.pb"):
        print("LOG: SSD Mobilenet V2 COCO model found.")
    else:
        print("LOG: SSD Mobilenet V2 COCO model not found. Downloading...")
        download_model()
        print("LOG: SSD Mobilenet V2 COCO model downloaded.")

    model = tf.saved_model.load("ssd_mobilenetv2_coco")
    create_folder(output_directory)
    
    print("LOG: Running...")
    # Process all images in the input folder
    for filename in os.listdir(input_image_folder):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith(".webp") or filename.endswith(".bmp"):
            input_image_path = os.path.join(input_image_folder, filename)
            object_detection(input_image_path, output_directory)
    print("LOG: Done.")
