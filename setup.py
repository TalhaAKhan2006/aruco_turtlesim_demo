from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'aruco_turtlesim_demo'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
         glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='F.L.O.R.A.L. Team',
    maintainer_email='student@example.com',
    description='ROS 2 Jazzy OpenCV ArUco to turtlesim demonstration',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'aruco_detector = aruco_turtlesim_demo.aruco_detector:main',
            'turtle_controller = aruco_turtlesim_demo.turtle_controller:main',
        ],
    },
)
