from setuptools import find_packages, setup
from glob import glob

package_name = 'autonomous_tb3'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*')),
        ('share/' + package_name + '/config', glob('config/*')),
        ('share/' + package_name + '/world', glob('world/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='tomato',
    maintainer_email='tomato@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sdf_spawner = autonomous_tb3.sdf_spawner:main',
            'commander = autonomous_tb3.commander:main'
        ],
    },
)
