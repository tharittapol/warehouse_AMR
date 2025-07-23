import os
from glob import glob
from setuptools import setup

package_name = 'jetrover_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.*'))),
        (os.path.join('share', package_name, 'urdf'), glob(os.path.join('urdf', '*.*'))),
        (os.path.join('share', package_name, 'rviz'), glob(os.path.join('rviz', '*.*'))),
        (os.path.join('share', package_name, 'meshes/acker'), glob(os.path.join('meshes/acker', '*.*'))),
        (os.path.join('share', package_name, 'meshes/arm'), glob(os.path.join('meshes/arm', '*.*'))),
        (os.path.join('share', package_name, 'meshes/common'), glob(os.path.join('meshes/common', '*.*'))),
        (os.path.join('share', package_name, 'meshes/gripper'), glob(os.path.join('meshes/gripper', '*.*'))),
        (os.path.join('share', package_name, 'meshes/mecanum'), glob(os.path.join('meshes/mecanum', '*.*'))),
        (os.path.join('share', package_name, 'meshes/tank'), glob(os.path.join('meshes/tank', '*.*'))),

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='1270161395@qq.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
