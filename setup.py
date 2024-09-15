from setuptools import setup, find_packages

setup(
    name='dcs_bios_connector',
    version='1.2',
    description='Allows easy access to dcs bios state and sending of commands',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Papi Planes',
    author_email='papiplanesfly@gmail.com',
    url='https://github.com/papiplanes/dcs_bios_connector',
    packages=find_packages(), 
    package_data={
        'dcs_bios_connector': ['json/*.json'],
    },
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
