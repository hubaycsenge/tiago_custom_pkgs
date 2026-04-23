import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'tiago_audio_behaviours'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'soundfiles'), glob('soundfiles/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='csengeubay@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'tiago_test_sound = tiago_audio_behaviours.tiago_test_sound:main',
            'tiago_nav_recov_sound = tiago_audio_behaviours.tiago_nav_recov_sound:main',
        ],
    },
)
