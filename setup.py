from setuptools import setup, find_packages

setup(
    name='dcs_bios_connector',                  # Package name
    version='0.1.0',                    # Version
    description='Allows easy access to dcs bios state and sending of commands',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Papi Planes',
    author_email='papiplanesfly@gmail.com',
    url='https://github.com/yourusername/my_package',
    packages=find_packages(), 
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
