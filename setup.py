from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="object_extraction",
    version="1.0.0",
    description="GUI application can used for detecting similar objects in a picture",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/nvakhilnair/Object-Extraction",
    author="Akhil",
    author_email="MadeWithPY009@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=["PyQt4>=4.11.4","opencv-python>=4.2.0.34","docutils>=0.3","numpy>=1.18.3","Pillow==7.1.1"],
    scripts=["object_extraction.py"],
    package_data={'data': ['logo.png','icon.ico']},
    include_package_data=True,
    
)
