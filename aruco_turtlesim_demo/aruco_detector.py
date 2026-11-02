#!/usr/bin/env python3

import cv2
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class ArucoDetectorNode(Node):
    """Read a camera, detect 6x6 ArUco markers, and publish their IDs."""

    def __init__(self):
        super().__init__('aruco_detector')

        self.declare_parameter('camera_index', 2)
        self.declare_parameter('show_window', True)
        self.declare_parameter('publish_rate_hz', 10.0)

        camera_index = self.get_parameter('camera_index').value
        self.show_window = self.get_parameter('show_window').value
        rate = float(self.get_parameter('publish_rate_hz').value)

        # Six target markers: IDs 1 through 6.
        self.target_ids = {1, 2, 3, 4, 5, 6}

        self.publisher = self.create_publisher(Int32, '/aruco_marker_id', 10)

        self.camera = cv2.VideoCapture(int(camera_index))
        if not self.camera.isOpened():
            self.get_logger().error(
                f'Could not open camera index {camera_index}. '
                'Try camera_index:=0 or another available index.'
            )

        # DICT_6X6_250 means 6x6 markers with IDs 0-249.
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_6X6_250
        )
        self.aruco_params = cv2.aruco.DetectorParameters()

        # OpenCV >= 4.7 uses ArucoDetector. Older OpenCV versions use
        # cv2.aruco.detectMarkers().
        self.modern_api = hasattr(cv2.aruco, 'ArucoDetector')
        if self.modern_api:
            self.detector = cv2.aruco.ArucoDetector(
                self.aruco_dict, self.aruco_params
            )
            self.get_logger().info('Using modern ArucoDetector API.')
        else:
            self.detector = None
            self.get_logger().warn(
                'ArucoDetector API not available; using legacy detectMarkers API.'
            )

        self.last_marker_id = None
        self.timer = self.create_timer(1.0 / max(rate, 1.0), self.process_frame)

        self.get_logger().info(
            'ArUco detector started. Target IDs: 1, 2, 3, 4, 5, 6.'
        )

    def process_frame(self):
        if not self.camera.isOpened():
            return

        success, frame = self.camera.read()
        if not success:
            self.get_logger().warn('Failed to grab camera frame.')
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.modern_api:
            corners, ids, rejected = self.detector.detectMarkers(gray)
        else:
            corners, ids, rejected = cv2.aruco.detectMarkers(
                gray, self.aruco_dict, parameters=self.aruco_params
            )

        detected_target = None

        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            for marker_id in ids.flatten():
                marker_id = int(marker_id)

                if marker_id in self.target_ids:
                    detected_target = marker_id

                    # Only publish when the detected target changes.
                    # This prevents one marker from repeatedly triggering
                    # the same turtle command every camera frame.
                    if marker_id != self.last_marker_id:
                        msg = Int32()
                        msg.data = marker_id
                        self.publisher.publish(msg)

                        self.get_logger().info(
                            f'[FOUND] ArUco ID {marker_id} detected -> published'
                        )
                    break

        # No target currently visible.
        if detected_target is None:
            self.last_marker_id = None
        else:
            self.last_marker_id = detected_target

        if self.show_window:
            cv2.imshow('ArUco Scanner', frame)
            # Required for OpenCV's GUI event processing.
            cv2.waitKey(1)

    def destroy_node(self):
        if hasattr(self, 'camera') and self.camera.isOpened():
            self.camera.release()
        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ArucoDetectorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
