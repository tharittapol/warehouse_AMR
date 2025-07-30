from setuptools import find_packages, setup

package_name = 'slam'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name + '/launch', ['launch/slam_toolbox.launch.py']),
        ('share/' + package_name + '/config', ['config/slam_toolbox_params.yaml']),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Tharittapol Takhumsuk',
    maintainer_email='tharitpol.big@gmail.com',
    description='SLAM Toolbox Launch',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
