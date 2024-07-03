import csv
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

def create_xml_annotation(image_info, annotations, output_dir):
    annotation = ET.Element("annotation")
    
    folder = ET.SubElement(annotation, "folder")
    folder.text = "input"
    
    filename = ET.SubElement(annotation, "filename")
    filename.text = image_info["filename"]
    
    path = ET.SubElement(annotation, "path")
    path.text = image_info["path"]
    
    source = ET.SubElement(annotation, "source")
    database = ET.SubElement(source, "database")
    database.text = "Unknown"
    
    size = ET.SubElement(annotation, "size")
    width = ET.SubElement(size, "width")
    width.text = str(image_info["width"])
    height = ET.SubElement(size, "height")
    height.text = str(image_info["height"])
    depth = ET.SubElement(size, "depth")
    depth.text = "3"
    
    segmented = ET.SubElement(annotation, "segmented")
    segmented.text = "0"
    
    for ann in annotations:
        obj = ET.SubElement(annotation, "object")
        name = ET.SubElement(obj, "name")
        name.text = ann["label"]
        
        pose = ET.SubElement(obj, "pose")
        pose.text = "Unspecified"
        
        truncated = ET.SubElement(obj, "truncated")
        truncated.text = "0"
        
        difficult = ET.SubElement(obj, "difficult")
        difficult.text = "0"
        
        bndbox = ET.SubElement(obj, "bndbox")
        xmin = ET.SubElement(bndbox, "xmin")
        xmin.text = str(ann["xmin"])
        ymin = ET.SubElement(bndbox, "ymin")
        ymin.text = str(ann["ymin"])
        xmax = ET.SubElement(bndbox, "xmax")
        xmax.text = str(ann["xmax"])
        ymax = ET.SubElement(bndbox, "ymax")
        ymax.text = str(ann["ymax"])
    
    xmlstr = minidom.parseString(ET.tostring(annotation)).toprettyxml(indent="   ")
    output_file = os.path.join(output_dir, f"{os.path.splitext(image_info['filename'])[0]}.xml")
    
    with open(output_file, "w") as f:
        f.write(xmlstr)
    
    print(f"Annotations for {image_info['filename']} saved to {output_file}")

def csv_to_openlabeler_xml(csv_file, output_dir, image_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    image_data = {}
    
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            image = row["image"]
            label = row["label"]
            xmin = int(float(row["xmin"]))
            ymin = int(float(row["ymin"]))
            xmax = int(float(row["xmax"]))
            ymax = int(float(row["ymax"]))
            
            if image not in image_data:
                image_path = os.path.join(image_dir, image)
                image_data[image] = {
                    "filename": image,
                    "path": image_path,
                    "width": 768,  # Update with actual width if available
                    "height": 432,  # Update with actual height if available
                    "annotations": []
                }
                
            image_data[image]["annotations"].append({
                "label": label,
                "xmin": xmin,
                "ymin": ymin,
                "xmax": xmax,
                "ymax": ymax
            })
    
    for image, data in image_data.items():
        create_xml_annotation(data, data["annotations"], output_dir)


csv_file = "/Users/zexianli/Desktop/tracking_results.csv"  # Path to your CSV file
output_dir = "/Users/zexianli/Desktop/project1/annotations"  # Path to the desired output directory
image_dir = "/Users/zexianli/Desktop/project1/input" 
# Example usage:
csv_to_openlabeler_xml(csv_file, output_dir, image_dir)

# Example usage:





