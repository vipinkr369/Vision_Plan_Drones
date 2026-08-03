import json
import random
import cv2
import numpy as np
import os

DATASET_JSON = "/home/psp/ros_ws/src/PDDL/vlm_training_data/dataset.json"
OUTPUT_JSONL = "/home/psp/ros_ws/src/PDDL/vlm_training_data/training_dataset2.jsonl"
IMAGES_DIR_PREFIX = "/home/psp/ros_ws/src/PDDL/vlm_training_data/"

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
        upper = np.array([180, 50, 255])
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
    
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
        
    largest_contour = max(contours, key=cv2.contourArea)
    if cv2.contourArea(largest_contour) < 50:
        return None
        
    x, y, w, h = cv2.boundingRect(largest_contour)
    # Return [xmin, ymin, xmax, ymax]
    return [x, y, x + w, y + h]

def generate_instruction(action_type, obj=None):
    if action_type == "home":
        prompts = [
            "plan: return home.",
            "plan: go to home location.",
            "plan: fly back to the base.",
            "plan: navigate home.",
            "plan: head to home."
        ]
        return random.choice(prompts)
    elif action_type == "fly_to":
        color = obj.get("color", "")
        category = obj.get("category", "object")
        prompts = [
            f"plan: go to the {color} {category}.",
            f"plan: fly to the {color} {category}.",
            f"plan: navigate to the {color} {category}.",
            f"plan: head over to the {color} {category}."
        ]
        return random.choice(prompts)
    elif action_type == "scanned":
        color = obj.get("color", "")
        category = obj.get("category", "object")
        prompts = [
            f"plan: scan the {color} {category}.",
            f"plan: inspect the {color} {category}.",
            f"plan: document the {color} {category}.",
            f"plan: analyze the {color} {category}."
        ]
        return random.choice(prompts)

def get_objects(image_data):
    gt = image_data.get("ground_truth", {})
    if "objects" in gt:
        return gt["objects"]
    elif "object" in gt:
        return [gt["object"]]
    return []

def main():
    with open(DATASET_JSON, 'r') as f:
        data = json.load(f)

    all_samples = []

    for split in ["train", "val", "test"]:
        if split not in data:
            continue
        for img_data in data[split]:
            image_path_rel = img_data["image_path"]
            image_path_abs = os.path.join(IMAGES_DIR_PREFIX, image_path_rel)
            
            objects = get_objects(img_data)
            if not objects:
                continue
                
            # Pre-compute valid bounding boxes
            valid_objects = []
            for obj in objects:
                color = obj.get("color")
                if color:
                    bbox = detect_object_bbox(image_path_abs, color)
                    if bbox:
                        obj["real_bbox"] = bbox
                        valid_objects.append(obj)
            
            if not valid_objects:
                print(f"No valid colored objects found in {image_path_abs}")
                continue

            for _ in range(100):
                rand_val = random.random()
                if rand_val < 0.1:
                    action_type = "home"
                    target_obj = None
                elif rand_val < 0.55:
                    action_type = "fly_to"
                    target_obj = random.choice(valid_objects)
                else:
                    action_type = "scanned"
                    target_obj = random.choice(valid_objects)

                instruction = generate_instruction(action_type, target_obj)

                if action_type == "home":
                    answer_dict = {
                        "objects": [{"id": "Home", "type": "target", "bbox": [0, 0, 0, 0]}],
                        "goal": "fly_to Home"
                    }
                else:
                    answer_dict = {
                        "objects": [{"id": target_obj["id"], "type": "target", "bbox": target_obj["real_bbox"]}],
                        "goal": f"fly_to {target_obj['id']}" if action_type == "fly_to" else f"scanned {target_obj['id']}"
                    }

                sample = {
                    "image_path": image_path_rel,
                    "qa": [
                        {
                            "question": instruction,
                            "answer": json.dumps(answer_dict)
                        }
                    ]
                }
                all_samples.append(sample)

    with open(OUTPUT_JSONL, 'w') as f:
        for sample in all_samples:
            f.write(json.dumps(sample) + "\n")

    print(f"Generated {len(all_samples)} samples in {OUTPUT_JSONL}")

if __name__ == "__main__":
    main()
