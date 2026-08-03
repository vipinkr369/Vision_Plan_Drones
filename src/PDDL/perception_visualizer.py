#!/usr/bin/env python3
import cv2
import json
import numpy as np
from pathlib import Path
from typing import Dict, Optional

def visualize_perception(
    rgb_image: np.ndarray,
    flight_plan: Dict,
    window_name: str = "Drone Perception",
    save_path: Optional[str] = None,
    show_window: bool = True
) -> np.ndarray:
    """
    Draws bounding boxes and 3D coordinates from a flight plan onto the image.
    
    Args:
        rgb_image: Image in RGB format.
        flight_plan: Dict containing "objects" with "bbox" and "estimated_coords".
        window_name: Name of the CV2 window to show.
        save_path: Path to save the resulting image.
        show_window: Whether to show the window via cv2.imshow.
        
    Returns:
        The visualized image in BGR format.
    """
    # Create copy and convert to BGR for OpenCV drawing and display
    vis_img = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    
    objects = flight_plan.get("objects", [])
    
    for obj in objects:
        if "point" in obj or "bbox" in obj:
            # coord data format [u, v, w, h] or [u, v]
            coord_data = obj.get("point", obj.get("bbox"))
            coord_data = [int(val) for val in coord_data]
            
            if len(coord_data) == 4:
                u, v, w, h = coord_data
            elif len(coord_data) == 2:
                u, v = coord_data[0] - 5, coord_data[1] - 5
                w, h = 10, 10
            else:
                continue
                
            coords = obj.get("estimated_coords", [0, 0, 0])
            obj_id = obj.get("id", "target")
            
            # Draw bounding box (or small box around point)
            cv2.rectangle(vis_img, (u, v), (u + w, v + h), (0, 255, 0), 2)
            
            # Prepare label text
            label = f"{obj_id}"
            
            # Label background
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(vis_img, (u, v - th - 10), (u + tw + 10, v), (0, 255, 0), -1)
            
            # Draw text
            cv2.putText(
                vis_img, label, (u + 5, v - 7),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA
            )
            
    if save_path:
        cv2.imwrite(str(save_path), vis_img)
        print(f"✓ Saved visualization to {save_path}")
        
    if show_window:
        cv2.imshow(window_name, vis_img)
        cv2.waitKey(1)
        
    return vis_img

if __name__ == "__main__":
    # Example usage as a ROS node for continuous visualization
    import rclpy
    from rclpy.node import Node
    from sensor_msgs.msg import Image
    from cv_bridge import CvBridge
    
    class VisualizerNode(Node):
        def __init__(self):
            super().__init__('perception_visualizer')
            self.bridge = CvBridge()
            self.flight_plan_path = Path("/home/psp/ros_ws/src/vpdrones/src/sjtu_drone/vpdrones/flight_plan.json")
            
            self.sub = self.create_subscription(
                Image,
                '/drone/front/image_raw',
                self.callback,
                10
            )
            self.get_logger().info("Perception Visualizer started. Watching /drone/front/image_raw")
            
        def callback(self, msg):
            try:
                # Convert ROS image to RGB for the function
                rgb_image = self.bridge.imgmsg_to_cv2(msg, "rgb8")
                
                if self.flight_plan_path.exists():
                    with open(self.flight_plan_path, 'r') as f:
                        flight_plan = json.load(f)
                    
                    visualize_perception(rgb_image, flight_plan)
                else:
                    cv2.imshow("Drone Perception", cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR))
                    cv2.waitKey(1)
                    
            except Exception as e:
                self.get_logger().error(f"Visualizer error: {e}")

    def main():
        rclpy.init()
        node = VisualizerNode()
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            pass
        finally:
            cv2.destroyAllWindows()
            node.destroy_node()
            rclpy.shutdown()

    main()
