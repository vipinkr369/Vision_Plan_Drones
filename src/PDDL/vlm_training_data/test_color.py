import cv2
import numpy as np

def get_color_mask(hsv, color_name):
    masks = []
    if color_name == "red":
        lower1 = np.array([0, 100, 100])
        upper1 = np.array([10, 255, 255])
        lower2 = np.array([160, 100, 100])
        upper2 = np.array([180, 255, 255])
        masks.append(cv2.inRange(hsv, lower1, upper1))
        masks.append(cv2.inRange(hsv, lower2, upper2))
    elif color_name == "blue":
        lower = np.array([100, 100, 50])
        upper = np.array([130, 255, 255])
        masks.append(cv2.inRange(hsv, lower, upper))
    elif color_name == "green":
        lower = np.array([40, 50, 50])
        upper = np.array([90, 255, 255])
        masks.append(cv2.inRange(hsv, lower, upper))
    elif color_name == "yellow":
        lower = np.array([20, 100, 100])
        upper = np.array([40, 255, 255])
        masks.append(cv2.inRange(hsv, lower, upper))
    elif color_name == "orange":
        lower = np.array([10, 100, 100])
        upper = np.array([25, 255, 255])
        masks.append(cv2.inRange(hsv, lower, upper))
    elif color_name == "brown":
        lower = np.array([10, 50, 20])
        upper = np.array([20, 255, 200])
        masks.append(cv2.inRange(hsv, lower, upper))
    elif color_name == "purple":
        lower = np.array([125, 50, 50])
        upper = np.array([150, 255, 255])
        masks.append(cv2.inRange(hsv, lower, upper))
    elif color_name == "white":
        lower = np.array([0, 0, 200])
        upper = np.array([180, 50, 255]) # low saturation, high value
        masks.append(cv2.inRange(hsv, lower, upper))
    elif color_name == "black":
        lower = np.array([0, 0, 0])
        upper = np.array([180, 255, 40])
        masks.append(cv2.inRange(hsv, lower, upper))
    elif color_name == "gray":
        lower = np.array([0, 0, 40])
        upper = np.array([180, 50, 200])
        masks.append(cv2.inRange(hsv, lower, upper))
    else:
        # fallback empty mask
        return np.zeros(hsv.shape[:2], dtype=np.uint8)

    mask = masks[0]
    for m in masks[1:]:
        mask = cv2.bitwise_or(mask, m)
    return mask

def detect_object_bbox(image_path, color_name):
    img = cv2.imread(image_path)
    if img is None:
        return None
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = get_color_mask(hsv, color_name)
    
    # morphological ops to clean up
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
        
    # Find largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    if cv2.contourArea(largest_contour) < 50: # min area
        return None
        
    x, y, w, h = cv2.boundingRect(largest_contour)
    return [x, y, x + w, y + h]

if __name__ == "__main__":
    img_path = "/home/psp/ros_ws/src/PDDL/vlm_training_data/images/drone_img_015_high_forward_20260203_102952.png"
    # dataset says this image contains "green_crate_0016"
    print("Testing green object detection:", detect_object_bbox(img_path, "green"))
