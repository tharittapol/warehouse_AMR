from setuptools import find_packages, setup

package_name = 'navigation'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name + '/launch', ['launch/navigation_bringup.launch.py']),
        ('share/' + package_name + '/params', ['params/navigation_param.yaml']),
        ('share/' + package_name + '/maps', ['maps/house_sim_map.yaml']),
        ('share/' + package_name + '/maps', ['maps/house_sim_map.pgm']),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Tharittapol Takhumsuk',
    maintainer_email='tharitpol.big@gmail.com',
    description='Navigation package wrapper for ROS2',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
