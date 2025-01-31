import os
import xml.etree.ElementTree as ET

# Define paths
data_dir = "dataset"
sets = ["train", "test"]
classes = ["aqua","chitato","indomie","pepsodent","shampoo","tissue"]

def convert_voc_to_yolo(annotations_dir, images_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for xml_file in os.listdir(annotations_dir):
        if not xml_file.endswith(".xml"):
            continue

        tree = ET.parse(os.path.join(annotations_dir, xml_file))
        root = tree.getroot()

        # Get image dimensions
        size = root.find("size")
        width = int(size.find("width").text)
        height = int(size.find("height").text)

        # Create corresponding YOLO label file
        txt_file = os.path.join(output_dir, os.path.splitext(xml_file)[0] + ".txt")
        with open(txt_file, "w") as f:
            for obj in root.findall("object"):
                class_name = obj.find("name").text
                if class_name not in classes:
                    continue
                class_id = classes.index(class_name)

                bndbox = obj.find("bndbox")
                xmin = int(bndbox.find("xmin").text)
                ymin = int(bndbox.find("ymin").text)
                xmax = int(bndbox.find("xmax").text)
                ymax = int(bndbox.find("ymax").text)

                # Normalize coordinates
                x_center = ((xmin + xmax) / 2) / width
                y_center = ((ymin + ymax) / 2) / height
                box_width = (xmax - xmin) / width
                box_height = (ymax - ymin) / height

                # Write to file
                f.write(f"{class_id} {x_center} {y_center} {box_width} {box_height}\n")

for subset in sets:
    annotations_dir = os.path.join(data_dir, subset, "annotations")
    images_dir = os.path.join(data_dir, subset, "images")
    output_dir = os.path.join(data_dir, subset, "labels")
    convert_voc_to_yolo(annotations_dir, images_dir, output_dir)
