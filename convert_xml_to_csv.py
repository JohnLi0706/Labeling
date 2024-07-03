import os
import csv
import xml.etree.ElementTree as ET

def parse_object(obj, image_width, image_height):
    name = obj.find("name").text
    category = ''.join([i for i in name if not i.isdigit() and i != '-'])
    ID = ''.join([i for i in name if i.isdigit()])
    
    bndbox = obj.find("bndbox")
    xmin = int(bndbox.find("xmin").text)
    ymin = int(bndbox.find("ymin").text)
    xmax = int(bndbox.find("xmax").text)
    ymax = int(bndbox.find("ymax").text)
    
    width = xmax - xmin
    height = ymax - ymin
    
    left = xmin / image_width
    top = ymin / image_height
    width_norm = width / image_width
    height_norm = height / image_height
    
    return {
        "category": category,
        "ID": ID,
        "left": left,
        "top": top,
        "width": width_norm,
        "height": height_norm
    }

def xml_to_csv(xml_folder, output_csv):
    xml_files = [f for f in os.listdir(xml_folder) if f.endswith('.xml')]
    
    with open(output_csv, mode='w', newline='') as csv_file:
        fieldnames = ["frames", "ID", "category", "top", "left", "height", "width"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        for xml_file in xml_files:
            tree = ET.parse(os.path.join(xml_folder, xml_file))
            root = tree.getroot()
            
            filename = root.find("filename").text
            image_width = int(root.find("size/width").text)
            image_height = int(root.find("size/height").text)
            
            for obj in root.findall("object"):
                obj_data = parse_object(obj, image_width, image_height)
                writer.writerow({
                    "frames": filename,
                    "ID": obj_data["ID"],
                    "category": obj_data["category"],
                    "top": obj_data["top"],
                    "left": obj_data["left"],
                    "height": obj_data["height"],
                    "width": obj_data["width"]
                })
                
    print(f"Annotations saved to {output_csv}")

# Example usage:
xml_folder = "/Users/zexianli/Desktop/project1/annotations"  # Path to the folder containing XML files
output_csv = "/Users/zexianli/Desktop/project1/convertback_output.csv"  # Path to the output CSV file
xml_to_csv(xml_folder, output_csv)
