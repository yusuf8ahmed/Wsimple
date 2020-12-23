from os import path
from setuptools import setup, find_packages

def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()

def from_here(relative_path):
    return path.join(path.dirname(__file__), relative_path)

with open('requirements.txt') as f: 
    requirements = f.readlines() 
# source env/bin/activate

#? pypi
# rm -rf build dist Wsimple.egg-info
# python setup.py sdist bdist_wheel 
# twine upload --skip-existing dist/*

setup(
    name="Wsimple",
    version="1.0.5",
    author="Yusuf Ahmed",
    author_email="yusufahmed172@gmail.com",
    packages=find_packages(include=("images", "wsimple", "wsimple.api" )),
    description="Wsimple.py: a API(Web interface) for Wealthsimple Trade",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/yusuf8ahmed/Wsimple",
    install_requires=[
        "loguru==0.5.3",
        "requests==2.24.0"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    platforms = 'any',
    keywords ='wsimple',
    python_requires='>=3',
    zip_safe = False
)