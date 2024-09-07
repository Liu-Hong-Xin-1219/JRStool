import os
from PIL import Image
# Category name mapping
category_mapping = {'C': 0, 'L': 1, 'R': 2, 'U': 3, 'Y': 4}
def get_image_size(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height
def convert_annotation_file(input_folder, output_folder, filename,img_folder):
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)
    local_img_path=os.path.join(img_folder,filename.split('.')[0].replace('device','image3')+'.png')
    imgw,imgh=get_image_size(local_img_path)
    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            # Split category and bbox info
            if line=='\n':
                continue
            category, bbox = line.strip().split(':')
            
            # Get the mapped category number
            category_num = category_mapping.get(category[0], -1)  # Use first character of category, ignore the number
            
            if category_num == -1:
                continue  # Skip unknown categories
            
            # Write the new format (replace commas with spaces)
            bbox = bbox.replace(',', ' ')
            if XYWHR_YOLO_NORMED:
                assert bbox.startswith('0.')
            else:
                x,y,w,h,r=bbox.split(' ')
                x,y,w,h,r=float(x),float(y),float(w),float(h),float(r)
                x,y,w,h,r=x/imgw,y/imgh,w/imgw,h/imgh,r
                bbox="{:.18f} {:.18f} {:.18f} {:.18f} {:.18f}".format(x,y,w,h,r)
            new_line = f"{category_num} {bbox}\n"
            outfile.write(new_line)

def process_folder(input_folder, output_folder,img_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Process each txt file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            
            convert_annotation_file(input_folder, output_folder, filename,img_folder)

# Input and output folder paths
input_raw_xywhr_folder = "D:\pcbobb\oribboxlbl"
output_yolo_label_folder = "D:\pcbobb\labels"
img_folder="D:\pcbobb\images"
XYWHR_YOLO_NORMED=False
# Process all files
process_folder(input_raw_xywhr_folder, output_yolo_label_folder,img_folder)
