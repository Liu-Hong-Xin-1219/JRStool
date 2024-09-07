import cv2
import numpy as np
from math import sin,cos
from math import pi as PI
from math import radians as rad

import cv2
import numpy as np
from math import cos, sin, radians as rad

def draw_rotated_bbox2(image, x, y, w, h, angle):
    # Denormalize x, y, w, h (convert back to pixel values)
    img_height, img_width = image.shape[:2]
    x = x * img_width
    y = y * img_height
    w = w * img_width
    h = h * img_height

    # Calculate the rotation matrix for the top-left corner
    M = cv2.getRotationMatrix2D((x, y), angle, 1)  # Rotation matrix around top-left corner (x, y)

    # Define the rectangle points starting from the top-left corner
    rect_points = np.array([
        [x, y],
        [x + w, y],
        [x + w, y + h],
        [x, y + h]
    ])

    # Apply the rotation matrix to the rectangle points
    rotated_points = cv2.transform(np.array([rect_points]), M)[0]

    # Convert points to integer values
    rotated_points = np.int0(rotated_points)

    # Draw the rotated bounding box on the image
    cv2.drawContours(image, [rotated_points], 0, (0, 255, 0), 2)

# Example usage:
# Assuming 'image' is already loaded (e.g., using cv2.imread)
# draw_rotated_bbox(image, x, y, w, h, angle)

def draw_rotated_bbox(image, x, y, w, h, angle):
    # Denormalize x, y, w, h (convert back to pixel values)
    img_height, img_width = image.shape[:2]
    x = x * img_width
    y = y * img_height
    w = w * img_width
    h = h * img_height

    width,height,rot=w,h,angle
    rr=rad(rot)
    xx=x+width*(-cos(rr))/2+height*sin(rr)/2
    yy=y-width*sin(rr)/2+height*(-cos(rr))/2
    cv2.circle(image, (int(xx), int(yy)), 10, (255,255,0), -1)    # Calculate the center, size and angle
    center = (int(x), int(y))
    size = (int(w), int(h))
    
    # Create the rotated rectangle
    rect = (center, size, angle)
    
    # Get the 4 corner points of the rotated rectangle
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    
    # Draw the rotated rectangle on the image
    cv2.drawContours(image, [box], 0, (0, 255, 0), 2)

def process_txt_and_draw(image_path, txt_path, output_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image {image_path}")
    
    # Read the bounding box annotations from the txt file
    with open(txt_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        # Split the line into class_type and bounding box info
        parts = line.strip().split()
        if len(parts) != 6:
            continue  # Skip malformed lines
        
        # Extract the information
        class_type = parts[0]
        x, y, w, h, r = map(float, parts[1:])
        
        # Draw the rotated bounding box on the image
        draw_rotated_bbox(image, x, y, w, h, r)
    
    # Save the resulting image
    cv2.imwrite(output_path, image)
    print(f"Image with bounding boxes saved to {output_path}")

# Example usage
image_path = 'D:\pcbobb\images\\160_0_0_image3.png'  # Path to your input image
txt_path = 'D:\pcbobb\labels\\160_0_0_image3.txt'  # Path to your txt file with bounding box annotations
output_path = 'output_image2.jpg'  # Path to save the output image

process_txt_and_draw(image_path, txt_path, output_path)
