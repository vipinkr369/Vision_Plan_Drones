#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class DepthVisualizerNode(Node):
    def __init__(self):
        super().__init__('depth_visualizer')
        self.bridge = CvBridge()
        
        self.sub = self.create_subscription(
            Image,
            '/drone/front/depth/image_raw',
            self.callback,
            10
        )
        self.get_logger().info("Depth Visualizer started. Watching /drone/front/depth/image_raw")
        
    def callback(self, msg):
        try:
            # Convert ROS Image to OpenCV format. Depth is either 32FC1 or 16UC1
            depth_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
            
            # Handle NaNs and Infs (commonly present in depth maps)
            # Replace NaNs with a far distance (or 0 depending on preference)
            depth_image = np.nan_to_num(depth_image, nan=0.0, posinf=0.0, neginf=0.0)
            
            # Normalize the depth image to 0-255 for visualization
            # Find min and max excluding zeros to get a better color spread
            valid_mask = depth_image > 0
            if np.any(valid_mask):
                min_val = np.min(depth_image[valid_mask])
                max_val = np.max(depth_image[valid_mask])
                
                # Clip extreme depths (e.g. above 10 meters) to avoid losing contrast on near objects
                max_val = min(max_val, 10.0) # Assume 10.0 is max useful depth
                
                depth_image = np.clip(depth_image, min_val, max_val)
                
                depth_normalized = cv2.normalize(
                    depth_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U
                )
            else:
                depth_normalized = np.zeros_like(depth_image, dtype=np.uint8)
            
            # Apply a colormap for better visibility
            # COLORMAP_JET shows near objects in red/yellow, far in blue
            depth_colormap = cv2.applyColorMap(depth_normalized, cv2.COLORMAP_JET)
            
            # Display the image
            cv2.imshow("Drone Depth Perception", depth_colormap)
            cv2.waitKey(1)
            
        except Exception as e:
            self.get_logger().error(f"Visualizer error: {e}")

def main():
    rclpy.init()
    node = DepthVisualizerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        # Ensure rclpy shutdown is clean
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == "__main__":
    main()
